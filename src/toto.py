def calculate_earnings(*payouts):
    assert len(payouts) > 0
    max_payout = max(payouts)
    bet_factor = sum(max_payout / payout for payout in payouts)
    for index, payout in enumerate(payouts, start=1):
        bet = max_payout / payout / bet_factor
        winning = bet * payout
        # print('With a bet of {} on {}, the winnings are {}'.format(bet, index, winning))
    print('Guaranteed return: {:.0f}% - {}'.format(winning * 100, 1/sum([1/payout for payout in payouts])))


if __name__ == '__main__':
    calculate_earnings(4.45, 3.6, 1.9)
    calculate_earnings(4.45, 7.75, 7.75, 13.5, 1.9)
    calculate_earnings(1.5, 2.55)
    calculate_earnings(1.76, 1.9)
    calculate_earnings(1.2, 3.6)
    calculate_earnings(1.15, 4.45)
    calculate_earnings(7.7, 13.75, 23, 9.4, 5.7, 4.85, 35, 12.75, 2.8)
    calculate_earnings(4.25, 2.2, 2.33)
    calculate_earnings(3.85, 2.53, 2.15)
    calculate_earnings(4, 1.2)
    calculate_earnings(2.7, 1.4)
    calculate_earnings(5, 1.14)
    calculate_earnings(3.95, 1.31, 8.9)
    calculate_earnings(3.1, 2.53, 3.75, 5.9)
    calculate_earnings(3.3, 2.58, 2.56)
    calculate_earnings(4.7, 2.75, 2)
    calculate_earnings(1.14, 5)
    calculate_earnings(12.75, 21.5, 55, 100, 250, 250, 12.5, 30, 80, 200, 35, 80, 12.75, 6.05, 11.25, 45, 7.9, 8.45,
                       13.5, 28.5, 70, 125, 7.8, 12.5, 26, 70, 22, 45, 24)
    calculate_earnings(13.5, 1.23, 5.4, 17.75)
    calculate_earnings(3, 1.01, 100)
