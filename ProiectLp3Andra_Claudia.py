import random

class UNOGame:
    def __init__(self, players):
        self.deck = self.create_deck()
        self.discard_pile = []
        self.players = players
        self.current_player = None
        self.direction = 1
        self.winner = None

    def create_deck(self):
        colors = ['Rosu', 'Verde', 'Albastru', 'Galben']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        special_cards = ['Schimb directia', 'Pune 2', 'Pune 4']
        deck = []
        
        for color in colors:
            for number in numbers:
                deck.append(color + ' ' + number)
                if number != '0':
                    deck.append(color + ' ' + number)
        
        for _ in range(4):
            deck.append('Schimb directia')
            deck.append('Pune 2')
            deck.append('Schimb culoarea')
            deck.append('Pune 4')
        
        random.shuffle(deck)
        return deck

    def deal_initial_cards(self):
        for _ in range(7):
            for player in self.players:
                card = self.deck.pop()
                player['hand'].append(card)

    def start_game(self):
        self.current_player = random.choice(self.players)
        self.discard_pile.append(self.deck.pop())

        self.deal_initial_cards()

        while not self.winner:
            self.show_game_state()
            self.play_turn()
            self.check_winner()

    def show_game_state(self):
        print('Cartea de deasupra: ', self.discard_pile[-1])
        print('Mana ta:', self.current_player['hand'])

    def play_turn(self):
        played_card = None
        valid_cards = self.get_valid_cards()

        if valid_cards:
            played_card = self.current_player['play'](valid_cards)
        else:
            print("Nu ai o carte validă. Tragi o carte din pachet.")
            self.draw_card(self.current_player, 1)

        if played_card:
            self.discard_pile.append(played_card)
            self.current_player['hand'].remove(played_card)

            if 'Schimb directia' in played_card:
                self.direction *= -1
            elif 'Pune 2' in played_card:
                next_player = self.get_next_player()
                self.draw_card(next_player, 2)
            elif 'Schimb culoarea' in played_card:
                new_color = self.current_player['choose_color']()
                print('Culoarea schimbă în:', new_color)
            elif 'Pune 4' in played_card:
                next_player = self.get_next_player()
                self.draw_card(next_player, 4)
                new_color = self.current_player['choose_color']()
                print('Culoarea schimbă în:', new_color)

        self.current_player = self.get_next_player()

    def get_valid_cards(self):
        top_card = self.discard_pile[-1]
        valid_cards = [card for card in self.current_player['hand'] if self.check_valid_card(card, top_card)]
        return valid_cards

    def check_valid_card(self, card, top_card):
        if card == 'Schimb culoarea' or card == 'Pune 4':
            return True
        elif card.split()[0] in top_card.split()[0] or card.split()[1] in top_card.split()[1]:
            return True
        return False

    def draw_card(self, player, num_cards):
        for _ in range(num_cards):
            if self.deck:
                player['hand'].append(self.deck.pop())
            else:
                self.deck = self.discard_pile[:-1]
                random.shuffle(self.deck)
                self.discard_pile = [self.discard_pile[-1]]

    def get_next_player(self):
        current_index = self.players.index(self.current_player)
        next_index = (current_index + self.direction) % len(self.players)
        return self.players[next_index]

    def check_winner(self):
        for player in self.players:
            if len(player['hand']) == 0:
                self.winner = player
                print('Felicitări! Jucătorul', player['name'], 'a câștigat!')

def choose_card(valid_cards):
    print("Alege o carte validă din lista de mai jos:")
    for i, card in enumerate(valid_cards):
        print(i + 1, ':', card)

    while True:
        choice = int(input("Introdu numărul corespunzător cărții: "))
        if choice in range(1, len(valid_cards) + 1):
            return valid_cards[choice - 1]

def choose_color():
    colors = ['Rosu', 'Verde', 'Albastru', 'Galben']
    print("Alege o culoare din lista de mai jos:")
    for i, color in enumerate(colors):
        print(i + 1, ':', color)

    while True:
        choice = int(input("Introdu numărul corespunzător culorii: "))
        if choice in range(1, len(colors) + 1):
            return colors[choice - 1]

if __name__ == "__main__":
    num_players = int(input("Introduceți numărul de jucători: "))

    players = []
    for i in range(num_players):
        name = input("Numele jucătorului " + str(i + 1) + ": ")
        players.append({'name': name, 'hand': [], 'play': choose_card, 'choose_color': choose_color})

    game = UNOGame(players)
    game.start_game()
