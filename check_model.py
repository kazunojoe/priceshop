import pandas as pd

# Change .csv files here
entry = pd.read_csv('./data/entry.csv')
product = pd.read_csv('./data/product_key.csv')

# Adding 'size column' into product dataFrame
def ft_regex(prod, rgx, colName):
	temp = prod['PSproductKey'].str.findall(rgx)
	size = []
	for i in temp:
		if len(i) == 0:
			i = '0'
		else:
			i = i[len(i) - 1]
		size.append(i)
	prod[colName] = size
ft_regex(product, r"\d+[GgTt][Bb]", "PSproductSize")

# Innitialize dataFrame and Series
entryName = entry['productName']
productBrand = product['brand'].str.lower().str.strip().unique()
productModelAndKey = pd.DataFrame({
	'productModel': product['PSmodelName'].str.split(' ', 1),
	'productKey': product['PSproductKey'],
	'productSize': product['PSproductSize'],
	'productType': product['category']
})

# Check if Brand in Entrytitle exists in database
def	check_brand(entryName, productBrand):
	temp = pd.Series(entryName.split(' '))
	for brand in productBrand:
		for value in temp:
			if (value.casefold() == brand.casefold()):
				return (brand)
	return ('jomama')

# Returns a "pd.Series()" of all models in Database based on brand
def check_model(brand, productModelAndKey):
	res = pd.DataFrame({})
	index = 1
	for i in range(len(productModelAndKey)):
		model = productModelAndKey['productModel'][i]
		key = productModelAndKey['productKey'][i]
		size = productModelAndKey['productSize'][i]
		type = productModelAndKey['productType'][i]
		if (brand.casefold() == model[0].casefold()):
			temp1 = pd.Series(model[1].strip().split('(', 1)[0].split('[', 1)[0].split('*', 1)[0].split(',', 1)[0].strip())
			temp2 = pd.Series(key)
			temp3 = pd.Series(size)
			temp4 = pd.Series(type)
			temp = pd.DataFrame({
				'index': index,
				'productModel': temp1,
				'productKey': temp2,
				'productSize': temp3,
				'productType': temp4
			})
			res = pd.concat([res, temp])
			index += 1
	res = res.set_index('index')
	return (res)

# # Test check_model() function here
# brand = 'Apple'
# models = check_model(brand, productModelAndKey)
# print(brand + ' ' + models['productModel'] + ', ' + models['productKey'] + ', ' + models['productSize'] + ', ' + models['productType'])

# # Output to models.csv
# models.to_csv("models.csv")
