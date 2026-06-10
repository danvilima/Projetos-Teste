# data.py

GROUPS = {
    "A": ["🇲🇽 México", "🇿🇦 África do Sul", "🇰🇷 Coreia do Sul", "🇨🇿 República Tcheca"],
    "B": ["🇨🇦 Canadá", "🇧🇦 Bósnia", "🇶🇦 Catar", "🇨🇭 Suíça"],
    "C": ["🇧🇷 Brasil", "🇲🇦 Marrocos", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escócia"],
    "D": ["🇺🇸 Estados Unidos", "🇵🇾 Paraguai", "🇦🇺 Austrália", "🇹🇷 Turquia"],
    "E": ["🇩🇪 Alemanha", "🇨🇼 Curaçao", "🇨🇮 Costa do Marfim", "🇪🇨 Equador"],
    "F": ["🇳🇱 Holanda", "🇯🇵 Japão", "🇸🇪 Suécia", "🇹🇳 Tunísia"],
    "G": ["🇧🇪 Bélgica", "🇪🇬 Egito", "🇮🇷 Irã", "🇳🇿 Nova Zelândia"],
    "H": ["🇪🇸 Espanha", "🇨🇻 Cabo Verde", "🇸🇦 Arábia Saudita", "🇺🇾 Uruguai"],
    "I": ["🇫🇷 França", "🇸🇳 Senegal", "🇮🇶 Iraque", "🇳🇴 Noruega"],
    "J": ["🇦🇷 Argentina", "🇩🇿 Argélia", "🇦🇹 Áustria", "🇯🇴 Jordânia"],
    "K": ["🇵🇹 Portugal", "🇨🇩 RD Congo", "🇺🇿 Uzbequistão", "🇨🇴 Colômbia"],
    "L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra", "🇭🇷 Croácia", "🇬🇭 Gana", "🇵🇦 Panamá"]
}

# Fixed Round of 32 matchups
# Format: { match_id: (home_slot, away_slot) }
R32_FIXED = {
    73: ("2º Grupo A", "2º Grupo B"),
    75: ("1º Grupo F", "2º Grupo C"),
    76: ("1º Grupo C", "2º Grupo F"),
    78: ("2º Grupo E", "2º Grupo I"),
    83: ("2º Grupo K", "2º Grupo L"),
    84: ("1º Grupo H", "2º Grupo J"),
    86: ("1º Grupo J", "2º Grupo H"),
    88: ("2º Grupo D", "2º Grupo G")
}

# Third place match constraints
# Match: (Fixed Winner, Allowed 3rd place groups)
R32_THIRD_PLACE = {
    74: ("1º Grupo E", ["A", "B", "C", "D", "F"]),
    77: ("1º Grupo I", ["C", "D", "F", "G", "H"]),
    79: ("1º Grupo A", ["C", "E", "F", "H", "I"]),
    80: ("1º Grupo L", ["E", "H", "I", "J", "K"]),
    81: ("1º Grupo D", ["B", "E", "F", "I", "J"]),
    82: ("1º Grupo G", ["A", "E", "H", "I", "J"]),
    85: ("1º Grupo B", ["E", "F", "G", "I", "J"]),
    87: ("1º Grupo K", ["D", "E", "I", "J", "L"])
}

# Next rounds flow (Winner of Match X vs Winner of Match Y -> Match Z)
KNOCKOUT_BRACKET = {
    "R16": {
        89: (73, 74),
        90: (75, 76),
        91: (77, 78),
        92: (79, 80),
        93: (81, 82),
        94: (83, 84),
        95: (85, 86),
        96: (87, 88)
    },
    "QF": {
        97: (89, 90),
        98: (91, 92),
        99: (93, 94),
        100: (95, 96)
    },
    "SF": {
        101: (97, 98),
        102: (99, 100)
    },
    "FINAL": {
        104: (101, 102) # Final
    },
    "THIRD_PLACE": {
        103: (101, 102) # Losers of 101 and 102
    }
}
