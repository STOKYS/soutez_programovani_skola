def fnc_read_file(file):
    with open(file, encoding='utf8') as f:
        t = f.read().split('\n')
        return t


def fnc_repeating_decimal(numr, denr):

	res = ''
	mp = {}

	rem = numr % denr
	while rem != 0 and rem not in mp:
		mp[rem] = len(res)
		rem = rem * 10
		res_part = rem // denr
		res += str(res_part)
		rem = rem % denr

	print(f'{numr} / {denr} = {numr / denr}')

	if rem == 0:
		print(f'Perioda: 0')
	else:
		print(f'Perioda: {res[mp[rem]:]}')

	if rem == 0:
		print(f'Predperioda: {str(numr / denr)}')
	else:
		print(f'Predperioda: {str(numr / denr).split(str(rem), 1)[0]}')

def main():
	data = fnc_read_file('input.txt')
	print(data)
	for x in data:
		fnc_repeating_decimal(1, int(x))


if __name__ == '__main__':
	main()
