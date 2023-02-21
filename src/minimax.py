"""
Minimax algorithm
"""

def score(node):
    """
    returns score of checkers game for black
    """
    state = ''
    for line in node.pieces:
        state += ''.join(line)
    return state.lower().count('b') - state.lower().count('r')
    
def best_move(node, depth):
    """
    returns best move at given depth
    """
    moves = node.get_moves()
    result = moves[0]

    if node.turn == 'b':
        bestscore = -10000

        for move in moves:
            child = node.copy()
            child.make_move(move)
            childscore = alphabeta(child, depth - 1, -10000, 10000)
            if childscore > bestscore:
                bestscore = childscore
                result = move
    else:
        bestscore = 10000

        for move in moves:
            child = node.copy()
            child.make_move(move)
            childscore = alphabeta(child, depth - 1, -10000, 10000)
            if childscore < bestscore:
                bestscore = childscore
                result = move
    
    return result


def alphabeta(node, depth, alpha, beta):
    """
    returns alpha beta score of a given node
    assumes node has attribute 'turn' and methods 'game_over()', 'get_moves()', 'make_move()' and 'copy()'
    """
    if node.game_over():
        return 10000 * (-1 if node.turn == 'b' else 1)
    elif depth == 0:
        return score(node)
    elif node.turn == 'b':
        moves = node.get_moves()
        
        for move in moves:
            child = node.copy()
            child.make_move(move)
            alpha = max(alpha, alphabeta(child, depth - 1, alpha, beta))
            if alpha > beta:
                break

        return alpha
    else:
        moves = node.get_moves()

        for move in moves:
            child = node.copy()
            child.make_move(move)
            beta = min(beta, alphabeta(child, depth - 1, alpha, beta))
            if beta < alpha:
                break
        
        return beta



