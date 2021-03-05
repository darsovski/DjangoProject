#(1) Returns all custumers from Custumer table
custumers = Custumer.objects.all()

#(2) Returns first custumer in table
firstCustumer = Custumer.objects.first()

#(3) Returns last custumer in table
firstCustumer = Custumer.objects.last()

#(4) Returns single custumer by name
custumerByName=Custumer.objects.get(name='Zoran Arsovski')

#(5) Returns single custumer by id
custumerByName=Custumer.objects.get(id='2')
