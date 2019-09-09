import re
import pprint
pp = pprint.PrettyPrinter(indent=4)

tester = None
serial = None

tests = []

def parsetest(test, obj = None):
  if obj == None:
    obj = {}

  if len(test) == 0:
    return obj
  
  # handle each possible data block:
  if 'TEST NUMBER' in test[0]:
    obj['testnum'] = re.findall(r'TEST NUMBER\s+(\d+)', test[0])[0]
    return parsetest(test[1:], obj)
  
  elif 'DATE' in test[0]:
    obj['date'] = re.findall(r'DATE\s+(\d\d-\w\w\w-\d\d)', test[0])[0]
    return parsetest(test[1:], obj)
  
  elif 'APP NO' in test[0]:
    obj['appno'] = re.findall(r'APP NO +([a-zA-Z0-9]+)\s*', test[0])[0]
    return parsetest(test[1:], obj)
  
  elif 'TEST MODE' in test[0]:
    obj['testmode'] = re.findall(r'TEST MODE *(.+) *', test[0])[0]
    return parsetest(test[1:], obj)
  
  elif 'SITE' in test[0]:
    obj['site'] = re.findall(r'SITE *(.*)', test[0])[0]
    obj['site1'] = re.findall(r'SITE1 *(.*)', test[1])[0]
    obj['site2'] = re.findall(r'SITE2 *(.*)', test[2])[0]
    return parsetest(test[3:], obj)
  
  elif 'USER' in test[0]:
    obj['user'] = re.findall(r'USER *(.*)', test[0])[0]
    return parsetest(test[1:], obj)
  
  elif 'VISUAL CHECK' in test[0]:
    obj['visual'] = re.findall(r'VISUAL CHECK *([PF])', test[0])[0]
    return parsetest(test[1:], obj)

  elif 'LEAD CONTINUITY' in test[0]:
    obj['ieccont'] = re.findall(r'LEAD CONTINUITY *([PF])', test[0])[0]
    ex = re.findall(r'EARTH *(.*?) *([PF])', test[1])
    obj['iecearth'] = ex[0][0]
    obj['iecearthpass'] = ex[0][1]
    obj['iecearthlimit'] = re.findall(r'LIMIT *(.*)', test[2])[0]
    return parsetest(test[3:], obj)
  
  elif 'INS' in test[0]:
    # for some reason my tester adds an extra entry for insulation tests
    if 'INS 1' in test[1]:
      obj['ins1voltage'] = re.findall(r'INS *(.*)', test[1])[0]
    elif 'INS 2' in test[1]:
      obj['ins2voltage'] = re.findall(r'INS *(.*)', test[1])[0]

  elif 'INS 1' in test[0]:
    ex = re.findall(r'INS 1 *(.*?) *([PF])', test[0])
    obj['ins1'] = ex[0][0]
    obj['ins1pass'] = ex[0][1]
    obj['ins1limit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)

  elif 'INS 2' in test[0]:
    ex = re.findall(r'INS 2 *(.*?) *([PF])', test[0])
    obj['ins2'] = ex[0][0]
    obj['ins2pass'] = ex[0][1]
    obj['ins2limit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'PN CONTINUITY' in test[0]:
    if 'TOUCH' in test[1]:
      ex = re.findall(r'TOUCH *(.*?) *([PF])', test[1])
      obj['touch'] = ex[0][0]
      obj['touchpass'] = ex[0][1]
      obj['touchlimit'] = re.findall(r'LIMIT *(.*)', test[2])[0]
      obj['touchpn'] = re.findall(r'PN CONTINUITY *([PF])', test[0])[0]
      return parsetest(test[3:], obj)
    elif 'LOAD' in test[1]:
      ex = re.findall(r'LOAD *(.*?) *([PF])', test[1])
      obj['load'] = ex[0][0]
      obj['loadpass'] = ex[0][1]
      obj['loadlimit'] = re.findall(r'LIMIT *(.*)', test[2])[0]
      obj['loadpn'] = re.findall(r'PN CONTINUITY *([PF])', test[0])[0]
      return parsetest(test[3:], obj)

  elif 'CURRENT' in test[0]:
    ex = re.findall(r'CURRENT *(.*?) *([PF])', test[0])
    obj['current'] = ex[0][0]
    obj['currentpass'] = ex[0][1]
    obj['currentlimit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'LKGE' in test[0]:
    ex = re.findall(r'LKGE *(.*?) *([PF])', test[0])
    obj['lkge'] = ex[0][0]
    obj['lkgepass'] = ex[0][1]
    obj['lkgelimit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'BOND RANGE' in test[0]:
    obj['earthbondcurrent'] = re.findall(r'BOND RANGE *(.*)', test[0])[0]
    ex = re.findall(r'EARTH *(.*?) *([PF])', test[1])
    obj['earthbond'] = ex[0][0]
    obj['earthbondpass'] = ex[0][1]
    obj['earthbondlimit'] = re.findall(r'LIMIT *(.*)', test[2])[0]
    return parsetest(test[3:], obj)
  
  elif 'SUBST 1' in test[0]:
    ex = re.findall(r'SUBST 1 *(.*?) *([PF])', test[0])
    obj['subst1'] = ex[0][0]
    obj['subst1pass'] = ex[0][1]
    obj['subst1limit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'SUBST 2' in test[0]:
    ex = re.findall(r'SUBST 2 *(.*?) *([PF])', test[0])
    obj['subst2'] = ex[0][0]
    obj['subst2pass'] = ex[0][1]
    obj['subst2limit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'PROBE PELV' in test[0]:
    ex = re.findall(r'PROBE PELV *([PF])', test[0])
    obj['probepelvpass'] = ex[0]
    obj['currentlimit'] = re.findall(r'LIMIT *(.*)', test[1])[0]
    return parsetest(test[2:], obj)

  elif 'LOC1' in test[0]:
    obj['loc1'] = re.findall(r'LOC1 *(.*)', test[0])[0]
    obj['loc2'] = re.findall(r'LOC2 *(.*)', test[1])[0]
    return parsetest(test[2:], obj)
  
  elif 'DES1' in test[0]:
    obj['des1'] = re.findall(r'DES1 *(.*)', test[0])[0]
    obj['des2'] = re.findall(r'DES2 *(.*)', test[1])[0]
    obj['des3'] = re.findall(r'DES3 *(.*)', test[2])[0]
    return parsetest(test[3:], obj)
  
  elif 'TEXT1' in test[0]:
    obj['note'] = re.findall(r'TEXT1 *(.*)', test[0])[0] + re.findall(r'TEXT2 *(.*)', test[1])[0]
    return parsetest(test[2:], obj)

  else:
    # unknown entry type, skip this line?
    print(test)
    return parsetest(test[1:], obj)


with open('rptest.FLK') as t:
  ls = t.readlines()
  tester = re.findall("MODEL *(.*) *?", ls[1])[0]
  serial = re.findall("SN *(.*) *?", ls[2])[0]
  testdata = ''.join(ls[4:-2])
  testdata = testdata.split('\n\n')
  print(f"Found {len(testdata)} tests.")
  for test in testdata:
    test = [l.rstrip() for l in test.split('\n')]
    data = parsetest(test, {})
    if data:
      tests.append(data)

print("----")
print("Parse done!")
print ("Tester: " + tester)
print ("Serial: " + serial)
pp.pprint(tests)