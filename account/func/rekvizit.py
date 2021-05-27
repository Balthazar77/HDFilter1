from dadata import Dadata
token = "d95e7606e5ded1dd1095eb2dc642f7734ce3f55e"
dadata = Dadata(token)
result = dadata.find_by_id(name="party", query="7707083893", kpp="540602001")
result2 = dadata.suggest(name="party", query="ООО Гудвил Запчасти")
print(result2)