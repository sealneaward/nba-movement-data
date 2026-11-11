"""
Possession labeling for NBA events.

Determines which team has possession for each event independently.
"""

import pandas as pd

# NBA team ID to abbreviation mapping
TEAM_ID_MAP = {
    1610612738: 'BOS',
    1610612751: 'BKN',
    1610612752: 'CLE',
    1610612761: 'TOR',
    1610612762: 'UTA',
    1610612766: 'CHA',
    1610612741: 'CHI',
    1610612743: 'DEN',
    1610612765: 'DET',
    1610612744: 'GSW',
    1610612745: 'HOU',
    1610612749: 'MIL',
    1610612748: 'LAL',
    1610612746: 'LAC',
    1610612764: 'MEM',
    1610612754: 'IND',
    1610612739: 'CLE',
    1610612742: 'DAL',
    1610612753: 'MIA',
    1610612761: 'TOR',
    1610612740: 'NOP',
    1610612752: 'CLE',
    1610612760: 'OKC',
    1610612755: 'PHI',
    1610612756: 'PHX',
    1610612757: 'POR',
    1610612761: 'TOR',
    1610612762: 'UTA',
    1610612764: 'MEM',
    1610612765: 'DET',
}


def get_team_abbreviation(team_id):
    """Convert NBA team ID to abbreviation."""
    return TEAM_ID_MAP.get(team_id)


def get_possession_team(row: pd.Series) -> str:
    """
    Determine the team in possession for a single event.
    
    Works independently for each event by analyzing the event type and player info.
    
    Args:
        row: A pandas Series representing a single event row
        
    Returns:
        Team abbreviation (str) for the team in possession, or None/empty for events
        where possession is unclear or not applicable.
        
    Event Logic:
        - Type 1 (Made FG): Shooting team has possession
        - Type 2 (Missed FG): Shooting team had possession
        - Type 3 (Free Throw): Shooting team has possession
        - Type 4 (Rebound): Rebounding team gains possession
        - Type 5 (Turnover): Stealing team gains possession
        - Type 6 (Foul): Defending team's possession state (PLAYER2_TEAM)
        - Type 7 (Violation): Unclear; marked as None
        - Type 10 (Jump Ball): Tip-to player (PLAYER3) gains possession
        - Types 8,9,12,13,18: Not applicable (substitution, timeout, period boundaries)
    """
    msg_type = row.get('EVENTMSGTYPE')
    
    # Handle NaN/missing values
    if pd.isna(msg_type):
        return None
    
    msg_type = int(msg_type)
    
    # Made field goal, missed field goal, free throw
    if msg_type in (1, 2, 3):
        team = row.get('PLAYER1_TEAM_ABBREVIATION')
        return team if not pd.isna(team) else None
    
    # Rebound
    if msg_type == 4:
        team = row.get('PLAYER1_TEAM_ABBREVIATION')
        if not pd.isna(team):
            return team
        
        # Fallback 1: Use PLAYER1_ID as team ID
        player1_id = row.get('PLAYER1_ID')
        if not pd.isna(player1_id):
            abbr = get_team_abbreviation(player1_id)
            if abbr:
                return abbr
        
        return None
    
    # Turnover - determine which team gains possession
    if msg_type == 5:
        home_desc = row.get('HOMEDESCRIPTION')
        visitor_desc = row.get('VISITORDESCRIPTION')
        
        # HOMEDESCRIPTION always describes HOME team actions
        # VISITORDESCRIPTION always describes VISITOR team actions
        
        has_steal_home = pd.notna(home_desc) and 'STEAL' in str(home_desc)
        has_steal_visitor = pd.notna(visitor_desc) and 'STEAL' in str(visitor_desc)
        
        # If STEAL in HOME: home team stole it and has possession
        # Stealer is typically in PLAYER2 when HOME describes the steal
        if has_steal_home:
            p2_team_id = row.get('PLAYER2_TEAM_ID')
            if not pd.isna(p2_team_id):
                return get_team_abbreviation(p2_team_id)
        
        # If STEAL in VISITOR: visitor team stole it and has possession
        # Stealer could be in PLAYER1 or PLAYER2 depending on event structure
        if has_steal_visitor:
            p2_team_id = row.get('PLAYER2_TEAM_ID')
            if not pd.isna(p2_team_id):
                return get_team_abbreviation(p2_team_id)
            # Fallback: try P1 if P2 fails
            p1_team_id = row.get('PLAYER1_TEAM_ID')
            if not pd.isna(p1_team_id):
                return get_team_abbreviation(p1_team_id)
        
        # No STEAL: one team turned over the ball
        if pd.isna(home_desc) or pd.isna(visitor_desc):
            # Get the turnover maker's team
            p1_team_id = row.get('PLAYER1_TEAM_ID')
            if not pd.isna(p1_team_id):
                return get_team_abbreviation(p1_team_id)
            
            # Fallback: check if PLAYER1_ID is a team ID
            player1_id = row.get('PLAYER1_ID')
            if not pd.isna(player1_id):
                player1_id_str = str(int(player1_id))
                if player1_id_str.startswith('161'):
                    return get_team_abbreviation(player1_id)

        
        return None
    
    # Foul - defensive team (the team that committed the foul)
    # Technical fouls have no PLAYER2 and don't change possession
    if msg_type == 6:
        team = row.get('PLAYER2_TEAM_ABBREVIATION')
        if not pd.isna(team):
            return team
        
        # Fallback: use PLAYER2_TEAM_ID
        p2_team_id = row.get('PLAYER2_TEAM_ID')
        if not pd.isna(p2_team_id):
            return get_team_abbreviation(p2_team_id)
        
        # No PLAYER2 = technical foul = no possession change
        return None
    
    # Violation - other team gets possession
    if msg_type == 7:
        # Violations (delay of game, kicked ball, etc.) result in other team getting possession
        p1_team_id = row.get('PLAYER1_TEAM_ID')
        if not pd.isna(p1_team_id):
            return get_team_abbreviation(p1_team_id)
        
        # Fallback: check if PLAYER1_ID is a team ID
        player1_id = row.get('PLAYER1_ID')
        if not pd.isna(player1_id):
            player1_id_str = str(int(player1_id))
            if player1_id_str.startswith('161'):
                return get_team_abbreviation(player1_id)
        
        return None
    
    # Jump ball - tip-to player (PLAYER3) gains possession
    if msg_type == 10:
        team = row.get('PLAYER3_TEAM_ABBREVIATION')
        return team if not pd.isna(team) else None
    
    # Substitution (8), Timeout (9), Period start (12), Period end (13), Player stats (18)
    # These don't indicate possession
    if msg_type in (8, 9, 12, 13, 18):
        return None
    
    return None


def add_possession_label(events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a possession_team column to an events dataframe.
    
    Args:
        events_df: DataFrame with event data
        
    Returns:
        DataFrame with new 'possession_team' column added
    """
    df = events_df.copy()
    
    # Find the two teams in this game and determine which is HOME vs VISITOR
    # by looking at the first non-NaN team ID in PLAYER1_TEAM_ID and finding its complement
    all_p1_team_ids = df['PLAYER1_TEAM_ID'].dropna().unique()
    game_teams = sorted([int(tid) for tid in all_p1_team_ids if not pd.isna(tid)])
    
    # For events with HOMEDESCRIPTION, PLAYER1 is typically from HOME team
    # For events with VISITORDESCRIPTION, PLAYER1 is typically from VISITOR team
    # But we need all possible team IDs from the game
    all_team_ids = pd.concat([
        df['PLAYER1_TEAM_ID'],
        df['PLAYER2_TEAM_ID'],
        df['PLAYER3_TEAM_ID']
    ]).dropna().unique()
    game_teams = sorted([int(tid) for tid in all_team_ids if not pd.isna(tid)])
    
    # Identify HOME vs VISITOR teams by checking which team appears in HOME events
    home_team_candidates = set()
    for idx, row in df.iterrows():
        if pd.notna(row.get('HOMEDESCRIPTION')):
            p1_tid = row.get('PLAYER1_TEAM_ID')
            if not pd.isna(p1_tid):
                home_team_candidates.add(int(p1_tid))
    
    # The team that appears most often in HOME events is the HOME team
    home_team_id = None
    if len(home_team_candidates) == 1:
        home_team_id = list(home_team_candidates)[0]
    elif len(home_team_candidates) > 1:
        # Pick the one that appears most
        team_counts = {}
        for idx, row in df.iterrows():
            if pd.notna(row.get('HOMEDESCRIPTION')):
                p1_tid = row.get('PLAYER1_TEAM_ID')
                if not pd.isna(p1_tid):
                    tid = int(p1_tid)
                    team_counts[tid] = team_counts.get(tid, 0) + 1
        if team_counts:
            home_team_id = max(team_counts, key=team_counts.get)
    
    # Determine visitor team
    visitor_team_id = None
    if home_team_id and len(game_teams) == 2:
        visitor_team_id = [t for t in game_teams if t != home_team_id][0]
    
    def get_possession_with_game_context(row):
        """Get possession team, using game context to find 'other' team if needed."""
        team = get_possession_team(row)
        
        # If we got a result, use it
        if not pd.isna(team):
            return team
        
        # For events with missing data, we need game context
        msg_type = row.get('EVENTMSGTYPE')
        if msg_type == 5 and home_team_id and visitor_team_id:
            home_desc = row.get('HOMEDESCRIPTION')
            visitor_desc = row.get('VISITORDESCRIPTION')
            has_steal_home = pd.notna(home_desc) and 'STEAL' in str(home_desc)
            has_steal_visitor = pd.notna(visitor_desc) and 'STEAL' in str(visitor_desc)
            
            # STEAL events with missing PLAYER2_TEAM_ID
            if has_steal_home:
                # HOME team stole the ball
                return get_team_abbreviation(home_team_id)
            
            if has_steal_visitor:
                # VISITOR team stole the ball
                return get_team_abbreviation(visitor_team_id)
            
            # Non-STEAL turnovers with missing player team data
            # Home team turned over → visitor gets possession
            if pd.notna(home_desc):
                return get_team_abbreviation(visitor_team_id)
            
            # Visitor team turned over → home gets possession
            if pd.notna(visitor_desc):
                return get_team_abbreviation(home_team_id)
        
        # Type 7 (Violation) - other team gets possession
        if msg_type == 7 and home_team_id and visitor_team_id:
            p1_team_id = row.get('PLAYER1_TEAM_ID')
            if not pd.isna(p1_team_id):
                p1_team_id = int(p1_team_id)
                # Return the OTHER team
                if p1_team_id == home_team_id:
                    return get_team_abbreviation(visitor_team_id)
                else:
                    return get_team_abbreviation(home_team_id)
        
        return team
    
    df['possession_team'] = df.apply(get_possession_with_game_context, axis=1)
    return df


if __name__ == '__main__':
    # Example usage
    df = pd.read_csv('data/events/0021500492.csv')
    df_labeled = add_possession_label(df)
    
    # Show sample output
    print("Sample events with possession labels:")
    display_cols = [
        'EVENTNUM', 'EVENTMSGTYPE', 'PLAYER1_NAME', 'PLAYER1_TEAM_ABBREVIATION',
        'PLAYER2_NAME', 'PLAYER2_TEAM_ABBREVIATION', 'possession_team'
    ]
    print(df_labeled[display_cols].head(20))
    
    # Summary statistics
    print("\n\nPossession Label Summary:")
    print(df_labeled['possession_team'].value_counts())
    print(f"\nEvents without clear possession: {df_labeled['possession_team'].isna().sum()}")
    
    # Check coverage by event type
    print("\n\nCoverage by Event Type:")
    for msg_type in sorted(df_labeled['EVENTMSGTYPE'].dropna().unique()):
        msg_type = int(msg_type)
        subset = df_labeled[df_labeled['EVENTMSGTYPE'] == msg_type]
        labeled = subset['possession_team'].notna().sum()
        total = len(subset)
        pct = (labeled / total * 100) if total > 0 else 0
        print(f"Type {msg_type:2d}: {labeled:3d}/{total:3d} labeled ({pct:5.1f}%)")
