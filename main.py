import Cards


def get_plays(sign, played):
    a = []
    for i in played:
        if sign in i:
            a.append(i)
    return a


def cards_assigner(cards):
    """
    This function assigns cards of different suits to different lists and adds them to a dictionary.
    """

    # Sort the cards in ascending order
    # and return the sorted list
    dictionary = {'C': [],
                  'D': [],
                  'H': [],
                  'S': []}
    for card in cards:
        dictionary[card[1]].append(card)
    for suit in dictionary:
        dictionary[suit].sort(key=lambda x: Cards.value[x], reverse=True)
    return dictionary


def card_sort(cards):
    """
    This function sorts the cards in descending order.
    """
    ret = cards_assigner(cards)
    clubs = ret['C']
    spades = ret['S']
    diamonds = ret['D']
    hearts = ret['H']
    list2 = []

    c = str(len(clubs)) + 'C'
    h = str(len(hearts)) + 'H'
    d = str(len(diamonds)) + 'D'
    dictionary = {
        c: clubs,
        h: hearts,
        d: diamonds,
    }
    list1 = [c, h, d]
    list1.sort(reverse=True)
    for i in list1:
        list2 = list2 + dictionary[i]
    return spades + list2


def get_cards(card_name):
    """
    This function returns suitable name of player's cards. Like, it takes '1S/0' and returns '1S'.
    """
    return card_name[0:2]


def logic(played, cards, history):
    # This is the main logic of the game.
    play = ''  # This is the variable for final card that we're returning
    same = 0  # Just to track sth
    spades = []  # To store spades
    clubs = []  # To store clubs
    remains = []  # To store remaining cards
    diamonds = []  # To store diamonds
    sign_match = []
    play_sorted = []
    hearts = []
    remaining_sorted = []
    sign_of_the_card = ''
    total_cards = cards_assigner(cards)
    spades = total_cards['S']
    clubs = total_cards['C']
    diamonds = total_cards['D']
    sign_remains = []
    hearts = total_cards['H']
    playable = []
    applicable_remains = []
    our_cards = []
    overall_history = []
    cards_arranged = card_sort(cards)
    total_played = []
    for dash in history:
        overall_history += dash[1]
    overall_history = list(map(get_cards, overall_history))
    # When no players have played before you, i.e. your turn is in the first throw of any round.
    played_cards = list(map(get_cards, played))  # Gets proper list of played card
    play_sorted = card_sort(played_cards)  # Sorts played cards
    total_played = card_sort(
        list(map(get_cards,
                 overall_history)) + played_cards)  # Gets overall history of cards that have been played

    sign_match = get_plays(sign_of_the_card,
                           play_sorted)  # Gets the list of played cards that have the same sign as the played card
    sign_match = card_sort(sign_match)  # Sorts the sign_match list
    remains = card_sort([z for z in Cards.cards if
                         z not in total_played])  # Gets the list of cards that have not been played yet
    sign_remains = cards_assigner(
        remains)  # Gets a dictionary of the cards that have not been played yet with their respective signs
    our_cards = cards_assigner(cards)
    if played == []:
        # When it's the first round
        if history == []:
            if '1S' in cards and 'KS' in cards and 'QS' in cards:  # If we have 'KS', 'QS' and '1S', it plays '1S' at the very beginning of the game so that we can make other player throw their spades
                play = '1S'
            elif '1C' in cards or '1D' in cards or '1H' in cards:
                play = [x for x in cards if '1' in x][
                    0]  # If we have '1C', '1D' or '1H', it plays '1C' or '1D' or '1H' at the very beginning of the game.
            else:
                play = card_sort(cards)[-1]  # Otherwise, it plays the lowest possible card
        # When it's not the first round
        elif history != []:
            applicable = [b for b in card_sort(cards) if b in clubs or b in diamonds or b in hearts]
            try:
                playable = [applicable[0], applicable[-1]]
            except:
                playable = spades
            if Cards.value[playable[0]] > Cards.value[sign_remains[playable[0][-1]][0]] and len(
                    sign_remains[playable[0][-1]]) > 10:
                play = playable[0]
            else:
                play = playable[-1]

    # When other players have played before you
    elif played != []:
        sign_of_the_card = played_cards[0][1]  # Gets the sign of the card that has been played
        applicable_remains = sign_remains[sign_of_the_card]
        # Gets the list of remaining cards that have the same sign as the played card
        # When it's the first round
        if history == []:
            for c in cards:
                if c[1] == sign_of_the_card:
                    playable.append(c)  # Gets the list of cards that we have that have the same sign as the played card
            if len(playable) < 1:  # If we no longer have cards with same sign,
                if spades != []:  # And if we have spades,
                    if len(cards_assigner(play_sorted)['S']) < 1:
                        playable = [spades[-1]]  # Spade of the lowest value is played
                    else:
                        for i in spades:
                            if Cards.value[i] > Cards.value[play_sorted[0]]:
                                playable = [i]
                else:
                    playable = list(i for i in cards if
                                    Cards.value[i] <= 5)  # If we don't have spades, we play cards of value 5 or less
                    if playable == []:
                        playable = [cards_arranged[
                                        -1]]  # If we don't have cards of value 5 or less, we play the lowest card that we have
                same = 1
            if same != 1:
                playable = card_sort(playable)  # If we have cards with same sign, we sort them
                if Cards.value[playable[0]] >= Cards.value[sign_remains[sign_of_the_card][0]] and len(
                        sign_remains[sign_of_the_card]) > 6:
                    play = playable[0]
                else:
                    for i in playable:
                        if Cards.value[i] > Cards.value[sign_match[0]]:
                            # And play the card with exactly higher value than already played card with the highest value
                            play = i
                    if play == '':
                        play = playable[-1]
            else:
                play = playable[
                    -1]  # If we do not have cards with same sign, we play the lowest spade card or lowest other card
            if play == '':
                # If we don't have higher cards with same sign, we play the last card of the list, i.e. the lowest value card of same sign
                play = cards_arranged[-1]

        elif history != []:
            for c in cards:
                if c[1] == sign_of_the_card:
                    playable.append(c)  # Gets the list of cards that we have that have the same sign as the played card
            if len(playable) < 1:  # If we no longer have cards with same sign,
                if spades != []:  # And if we have spades,
                    if len(cards_assigner(play_sorted)['S']) < 1:
                        playable = [spades[-1]]  # Spade of the lowest value is played
                    else:
                        for i in spades:
                            if Cards.value[i] > Cards.value[play_sorted[0]]:
                                playable = [i]
                            if playable == []:
                                playable = spades  # If we don't have spades, we play cards of value 5 or less
                else:
                    playable = list(i for i in cards if
                                    Cards.value[i] <= 5)  # If we don't have spades, we play cards of value 5 or less
                    if playable == []:
                        playable = [cards_arranged[
                                        -1]]  # If we don't have cards of value 5 or less, we play the lowest card that we have
                same = 1
            if same != 1:
                playable = card_sort(playable)  # If we have cards with same sign, we sort them

                if Cards.value[playable[0]] > Cards.value[sign_remains[sign_of_the_card][0]] and \
                        Cards.value[playable[0]] >= Cards.value[play_sorted[0]] and len(
                    sign_remains[sign_of_the_card]) - len(playable) > 6:
                    play = playable[0]
                else:
                    for i in playable:
                        if Cards.value[i] > Cards.value[sign_match[0]]:
                            # And play the card with exactly higher value than already played card with the highest value
                            play = i
                    if play == '':
                        play = playable[-1]
            else:
                play = playable[
                    -1]  # If we do not have cards with same sign, we play the lowest spade card or lowest other card
            if play == '':
                # If we don't have higher cards with same sign, we play the last card of the list, i.e. the lowest value card of same sign
                play = cards_arranged[-1]


    ######################################################################################

    print("Playable: " + str(playable))
    print('Total played' + str(play_sorted))
    print('sign match: ' + str(sign_match))
    print("Applicable throwable: " + str(applicable_remains))
    print("Remains: " + str(remains))
    print("total : " + str(total_played))
    print("Played Dictionary: " + str(sign_remains))
    print('sorted: ' + str(card_sort(cards)))
    # print('sign_remains: ' + str(sign_remains[Cards.dict2[sign_of_the_card]]))
    # print('idk' + str(Cards.value[sign_remains[Cards.dict2[sign_of_the_card]][0]]))
    print("Our cards: " + str(our_cards))
    print("Arranged cards: " + str(cards_arranged))
    print("Play (The final throw) : " + str(play))


cards = ['5S', '2S', '4H', '2H', 'TC', '6C']
played = ['7D/0', '6S/0', '5D/0']
history = [[1, ['1H/0', 'JH/0', '6H/0', '3H/0'], 1], [1, ['3D/0', '6D/0', '4D/0', 'TD/0'], 0],
           [0, ['5H/0', '8H/0', '7S/0', '9H/0'], 2], [2, ['2C/0', '8C/0', 'JC/0', 'QC/0'], 1],
           [1, ['9D/0', 'JD/0', '4S/0', '2D/0'], 3], [3, ['9C/0', 'KC/0', '5C/0', '4C/0'], 0],
           [0, ['7H/0', 'KH/0', '8S/0', 'TH/0'], 2]]

logic(played, cards, history)

print(cards_assigner(['1S', 'QH', '3H', '1C', 'QC', 'JC', '7C', '6C', '3C', '2C', '1D', 'KD', '3D']))
