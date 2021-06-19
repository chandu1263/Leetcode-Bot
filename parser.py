def parse(command):
  command = command.split(" ")
  output = []
  for each in command:
    if len(each) != 0:
      output.append(each)
  return output[1:]

def get_username(user_id):
  username = user_id.split("#")[0]
  return username