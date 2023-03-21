import e3db
from e3db.types import Search
import os
from dotenv import load_dotenv

#load env variables i.e. tokens from Tozny
load_dotenv()

# register our Alice token, so we can instantiate a new client to interact with TozStore
alice_token = os.getenv('alice_token')
client_name = 'Alice'
public_key, private_key = e3db.Client.generate_keypair()
alice_client_info = e3db.Client.register(
    alice_token, client_name, public_key)

alice_config = e3db.Config(
    alice_client_info.client_id,
    alice_client_info.api_key_id,
    alice_client_info.api_secret,
    public_key,
    private_key
)
# instantiate client obj
alice_client = e3db.Client(alice_config())

# register our Bruce token, so we can instantiate a new client to interact with TozStore
bruce_token = os.getenv('bruce_token')
client_name = 'Bruce'
public_key, private_key = e3db.Client.generate_keypair()
bruce_client_info = e3db.Client.register(
    bruce_token, client_name, public_key)
bruce_config = e3db.Config(
    bruce_client_info.client_id,
    bruce_client_info.api_key_id,
    bruce_client_info.api_secret,
    public_key,
    private_key
)
# instantiate client obj
bruce_client = e3db.Client(bruce_config())


# register our Judge token, so we can instantiate a new client to interact with TozStore
judge_token = os.getenv('judge_token')
client_name = 'Judge'
public_key, private_key = e3db.Client.generate_keypair()
judge_client_info = e3db.Client.register(judge_token, client_name, public_key)

judge_config = e3db.Config(
    judge_client_info.client_id,
    judge_client_info.api_key_id,
    judge_client_info.api_secret,
    public_key,
    private_key
)
# instantiate client obj
judge_client = e3db.Client(judge_config())


def play():
    '''
    This is our main function where
    user can play from command line:
    user can use the following commands:
    1 for rock, 2 for scissors, 3 for paper
    If more time, validate input better.
    paper beats rock. Scissors beats paper.Rock beats scissors.
    '''
    playing = True
    round = 0
    while playing:
        print('ROUND: ', round)
        print('1 for rock, 2 for scissors, 3 for paper')
        print('Alice goes first ')
        move = get_move_input()
        if round == 0:
            alice_record_id = set_Alice_input(move, round)
        else:
            update_Alice_input(move, alice_record_id, round)
            
        print('Bruce now your turn')
        move = get_move_input()
        if round == 0:
            bruce_record_id = set_Bruce_input(move, round)
        else:
            update_Bruce_input(move, bruce_record_id, round)
        if round == 0:
            Judge_record_id = set_judge_input(
                alice_record_id, bruce_record_id, round)
        else:
            update_judge_input(
                alice_record_id, bruce_record_id, Judge_record_id, round)

        # get winners read by alice/bruce
        winner_from_alice = winner_read_by_alice(Judge_record_id)
        winner_from_bruce = winner_read_by_bruce(Judge_record_id)
        print('winner read by Alice:', winner_from_alice)
        print('winner read by Bruce:', winner_from_bruce)
        print('******************************************')

        print('Continue Playing? any key for yes and n for no ')
        x = input()
        if x == 'n':
            playing = False
        else:
            playing = True
            round += 1


def winner_read_by_alice(judge_record_id):
    #read judge's record
    j = alice_client.read(judge_record_id)
    winner = j.data['winner']
    return winner


def winner_read_by_bruce(judge_record_id):
    #read judge's record
    j = bruce_client.read(judge_record_id)
    winner = j.data['winner']
    return winner


def update_Alice_input(player_move, record_id, round):
    '''
    Input is an string, a string, and an integer.
    
    This function takes record id of type string and
    updates client record (Alice).
    '''
    # data is decrypted with client key, verify signature
    original_record = alice_client.read(record_id)
    original_record.data['round'] = round
    original_record.data['move'] = player_move

    # get updated decrypted record
    updated_Alice_record = alice_client.update(original_record)

    print('Alices updated move: {0}'.format(updated_Alice_record.data['move']))


def set_Alice_input(player_move, round):
    '''
    Input is a string and an integer (input from command line).
    
    String represent a player's move, and integer represents round number
    this function creates a record of type player2 and writes
    player's move and round to their record type.
    Then client shares access to third party.
    
    Returns a string which is the record id. 
    '''
    record_type = 'player1'
    data = {'round': round,
            'move': player_move}
    record = alice_client.write(record_type, data)

    # share alice info with judge
    alice_client.share(record_type, judge_client_info.client_id)

    return record.meta.record_id


def update_Bruce_input(player_move, record_id, round):
    '''
    Input is a string, a string, and an integer.

    This function takes record id of type string and
    updates client record (Bruce).
    '''
    original_record = bruce_client.read(record_id)
    original_record.data['round'] = round
    original_record.data['move'] = player_move


    # get updated decrypted record
    updated_Bruce_record = bruce_client.update(original_record)
    print('Bruces updated move: {0}'.format(updated_Bruce_record.data['move']))


def set_Bruce_input(player_move, round):
    '''
    Input is a string and integer (input from command line).
    
    String represent a player's move, and integer represents round number
    this function creates a record of type player2 and writes
    player's move and round to their record type.
    Then client shares access to third party.
    
    Returns a string which is the record id.
    '''
    record_type = 'player2'
    data = {'round': round,
            'move': player_move}
    record = bruce_client.write(record_type, data)

    # share bruce_info with judge
    bruce_client.share(record_type, judge_client_info.client_id)

    return record.meta.record_id


def get_move_input():
    '''
    this function gets input from the command line
    1 is rock, 2 is scissor, 3 is paper
    returns a string, 'rock', 'scissor', or 'paper' 
    '''
    continue_get_input = True
    while continue_get_input == True:
        player_input = input()
        # make sure input is of type int
        player_input = validate_rps_move_input(player_input)
        
        # make sure input is between 0 and 4
        if player_input > 0 and player_input < 4:
            if player_input == 1:
                player_input = 'rock'
            elif player_input == 2:
                player_input = 'scissor'
            elif player_input == 3:
                player_input = 'paper'
            continue_get_input = False
            return player_input
        else:
            print('please enter valid input of type int')


def validate_rps_move_input(input):
    '''
    validate user input function
    '''
    try:
        return int(input)
    except TypeError:
        return -1


def update_judge_input(Alice_record_id, Bruce_record_id, judge_record_id, round):
    '''
    input is three strings and an integer:
    Alice's record id, Bruce's record id, Judge's record id and current round.
    
    Given access priveleges for Judge, Judge can read Alice's and Bruce's record
    Winner is determined by determine_winner_by judge function
    Judge's round and winner values are updated. 
    We have already given sharing priveleges to Alice and Bruce in set_judge_input
    
    returns the judge's record id so we can update it later
    '''
    
    # get alice and bruce's move
    a = judge_client.read(Alice_record_id)
    b = judge_client.read(Bruce_record_id)
    alice_move = a.data['move']
    bruce_move = b.data['move']

    # logic for winner Rock, Paper,Scissor. Returns alice or Bruce as winner
    winner = determine_winner_by_judge(alice_move, bruce_move)

    # update Judge's record
    original_record = judge_client.read(judge_record_id)
    original_record.data['round'] = round
    original_record.data['winner'] = winner
    updated_Judge_record = judge_client.update(original_record)
    print('Judge updated winner: {0}'.format(
        updated_Judge_record.data['winner']))


def set_judge_input(Alice_record_id, Bruce_record_id, round):
    '''
    Input is Alice's record id, Bruce's record id and current round.
    
    Because we shared judge id with alice and bruce, we can read their
    records. Their records show their move. We then determine the winner
    through determine_winner_by_judge function given alice's and bruce's
    move. We then create a new record for Judge client and store the round value 
    and first winner. Then we share that record with Alice and Bruce so they
    can read Judge's record respectively. 
    
    Returns the judge's record id so we can update it later
    '''

    a = judge_client.read(Alice_record_id)
    b = judge_client.read(Bruce_record_id)
    alice_move = a.data['move']
    bruce_move = b.data['move']

    # logic for winning Rock, Paper,Scissor. Returns alice or Bruce as winner
    winner = determine_winner_by_judge(alice_move, bruce_move)
    
    # write winner of first round to Judge's record
    record_type = 'Judgement'
    data = {'round': round,
            'winner': winner}
    judge_record = judge_client.write(record_type, data)
    
    # share judge_info with alice and bruce
    judge_client.share(record_type,  alice_client_info.client_id)
    judge_client.share(record_type,  bruce_client_info.client_id)

    # this is just so we can print our results
    original_record = judge_client.read(judge_record.meta.record_id)
    print('Judge updated winner: {0}'.format(
        original_record.data['winner']))

    return judge_record.meta.record_id


def determine_winner_by_judge(alice_move, bruce_move):
    '''
    Input is two strings: alice's move and bruce's move
    
    This function determines the winner by RPS logic
    
    Returns winner of type string
    '''
        
    # Combo paper and rock
    # if p1 has rock and p2 has paper
    if alice_move == 'rock' and bruce_move == 'paper':
        winner = 'bruce'
    # if p2 has rock and p1 has paper
    elif bruce_move == 'rock' and alice_move == 'paper':
        winner = 'alice'

    # Combo paper and scissors
    # if p1 has paper and p2 has scissor
    if alice_move == 'paper' and bruce_move == 'scissor':
        winner = 'bruce'
    # if p2 has paper and p1 has scissor
    elif bruce_move == 'paper' and alice_move == 'scissor':
        winner = 'alice'

    # Combo rock and scissors
    # if p1 has rock and p2 has scissor
    if alice_move == 'rock' and bruce_move == 'scissor':
        winner = 'alice'
    # if p2 has rock and p1 has scissor
    elif bruce_move == 'rock' and alice_move == 'scissor':
        winner = 'bruce'
        
    # if there is a tie
    if alice_move == bruce_move:
        winner = 'no winner'
    
    return winner

play()
