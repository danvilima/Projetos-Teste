# matching_algorithm.py
from data import R32_THIRD_PLACE

def match_third_places(selected_third_places):
    """
    selected_third_places: list of tuples (group_letter, team_name)
    e.g. [("A", "República Tcheca"), ("C", "Haiti"), ...] (Exactly 8)
    
    Returns a dict mapping match_id -> team_name, or None if no valid matching.
    """
    if len(selected_third_places) != 8:
        return None
        
    matches = list(R32_THIRD_PLACE.keys())
    group_to_team = {g: t for g, t in selected_third_places}
    
    def backtrack(match_idx, current_matching, used_groups):
        if match_idx == len(matches):
            return current_matching
            
        match_id = matches[match_idx]
        allowed_groups = R32_THIRD_PLACE[match_id][1]
        
        for g, t in selected_third_places:
            if g not in used_groups and g in allowed_groups:
                # Try assigning this team to this match
                used_groups.add(g)
                current_matching[match_id] = t
                
                result = backtrack(match_idx + 1, current_matching, used_groups)
                if result:
                    return result
                
                # Backtrack
                used_groups.remove(g)
                del current_matching[match_id]
                
        return None

    return backtrack(0, {}, set())
