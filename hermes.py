#Hermes trading bot
#Version 0.4 beta

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from bittrex import bittrex

f = open('config.txt', 'r')
identity = f.readline().split()[2]
password = f.readline().split()[2]
key = f.readline().split()[2]
secret = f.readline().split()[2]
deposit = f.readline().split()[2]
f.close()
bet = str(float(deposit)/4)

bot = bittrex.Bittrex(key, secret)

class Hermes(LineReceiver):

    def lineReceived(self, line):
        self.handle_COMMAND(line)

    def handle_COMMAND(self, command):
        data = command.decode().split()
        if data[0] != password:
            self.sendLine((identity + ': ' + 'Wrong password').encode())
        else:
            data.remove(data[0])
            if data[0] == 'buy':
                self.sendLine((identity + ': ' + 'Buying {}'.format(data[1])).encode())
                check = bot.buy_limit('BTC-{}'.format(data[1]), str(float(bet)/float(data[2])), data[2])
                if check['success']:
                    self.sendLine((identity + ': ' + 'success').encode())
                else:
                    self.sendLine((identity + ': ' + check['message']).encode())
                    
            elif data[0] == 'sell':
                self.sendLine((identity + ': ' + 'Selling {}'.format(data[1])).encode())
                balance = bot.get_balance(data[1])
                if balance['success']:
                    amount = balance['result']['Available']
                    check = bot.sell_limit('BTC-{}'.format(data[1]), amount, data[2])
                    if check['success']:
                        self.sendLine((identity + ': ' + 'success').encode())
                    else:
                        self.sendLine((identity + ': ' + check['message']).encode())
                else:
                    self.sendLine((identity + ': ' + balance['message']).encode())
                    
            elif data[0] == 'cancel':
                self.sendLine((identity + ': ' + 'Cancelling orders').encode())
                orders = bot.get_open_orders()
                if orders['success']:
                    for order in orders['result']:
                        check = bot.cancel(order['OrderUuid'])
                        if not check['success']:
                            self.sendLine((identity + ': ' + check['message']).encode())
                            break
                    else:
                        self.sendLine((identity + ': ' + 'success').encode())
                else:
                    self.sendLine((identity + ': ' + orders['message']).encode())

            elif data[0] == 'ping':
                self.sendLine((identity + ': ' + 'success').encode())

            else:
                self.sendLine((identity + ': ' + 'Unknown command').encode())
            
class HermesFactory(Factory):

    def buildProtocol(self, addr):
        return Hermes()

reactor.listenTCP(9091, HermesFactory())
reactor.run()
