from src.bot import FloppyBot

def init():
    bot = FloppyBot('', 0)
    bot.queue = {
            '01': {'channel' : '1'}
        }
    bot.garbage = {'02'}
    bot.hook = 'not_a_real_hook'
    bot.role = '1'
    return bot

def test_enqueue():
    bot = init()

    assert len(bot.queue) == 1

    # Check queue and fail
    bot.enqueue('01', {})
    assert len(bot.queue) == 1

    # Check garbage and fail
    bot.enqueue('02', {})
    assert len(bot.queue) == 1

    # Pass
    bot.enqueue('03', {})
    assert len(bot.queue) == 2

    # Invalid +time and fail
    bot.enqueue('60', {})
    assert len(bot.queue) == 2

    # Invalid -time and fail
    bot.enqueue('-01', {})
    assert len(bot.queue) == 2

def test_garbage_pickup():
    bot = init()

    assert len(bot.garbage) == 1

    # No cleanup
    bot.garbagePickup(17)
    assert len(bot.garbage) == 1

    # Cleanup
    bot.garbagePickup(18)
    assert len(bot.garbage) == 0

    # Wraparound item < time
    bot.garbage = {'45'}
    bot.garbagePickup(2)
    assert len(bot.garbage) == 0

    # Wraparound item > time
    bot.garbage = {'01'}
    bot.garbagePickup(30)
    assert len(bot.garbage) == 0