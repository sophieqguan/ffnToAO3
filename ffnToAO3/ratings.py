

# very unnecessary to make this a separate file, but maybe in the future
# ffnet will implement warnings or other ratings, so this may be expanded
def convert(ffn):
    if ffn == "Fiction K" or ffn == "Fiction K+":
        return "General Audiences"
    if ffn == "Fiction T":
        return "Teen And Up Audiences"
    if ffn == "Fiction M":
        return "Mature"
