

# very unnecessary to make this a separate file, but maybe in the future
# ffnet will implement warnings or other ratings, so this may be expanded
def convert(ffn):
    if ffn == "Fiction K" or ffn == "Fiction K+" or ffn == "K" or ffn == "K+":
        return "General Audiences"
    if ffn == "Fiction T" or ffn == "T":
        return "Teen And Up Audiences"
    if ffn == "Fiction M" or ffn == "M":
        return "Mature"
