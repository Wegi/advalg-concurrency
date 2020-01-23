# Asyncio is implemented in a single thread and has the concept of yielding
# processing time and of scheduling (most often when waiting for IO)

# Different ways to start coroutines. The easiest:
import asyncio

async def coroutine():
    print('in coroutine')
    return 'any result'

event_loop = asyncio.get_event_loop()
try:
    print('starting coroutine')
    coro = coroutine()
    print('entering event loop')
    return_value = event_loop.run_until_complete(coro)
    print('return value: ', return_value)
finally:
    print('closing event loop')
    event_loop.close()

# Loop stops when coroutine exits by returning. (while using run_until_complete)

# You can chain coroutines inside coroutines.
# This is useful when some event depends on another, but can still be run concurrently.


async def outer():
    print('in outer')
    print('waiting for result1')
    result1 = await phase1()
    print('waiting for result2')
    result2 = await phase2(result1)
    return result1, result2


async def phase1():
    print('in phase1')
    return 'result1'


async def phase2(arg):
    print('in phase2')
    return 'result2 derived from {}'.format(arg)


event_loop = asyncio.get_event_loop()
try:
    return_value = event_loop.run_until_complete(outer())
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()