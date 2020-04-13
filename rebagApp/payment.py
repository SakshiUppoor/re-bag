import razorpay
client = razorpay.Client(auth=("rzp_test_lSdtL3ABQA1Zv9", "qzvsbds0zZ1aigqQAhz61xfa"))
DATA={'amount': 50000, 'currency': 'INR', 'receipt': "123", 'payment_capture': 1}
client.order.create(data=DATA)
o= client.order.all()
print(o)
