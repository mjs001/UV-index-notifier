from utilities.convert_24hr import convert_24hr

def process_location(form_data):
  #form data is going to be json
  #I will need to retrieve vars for api keys for www.geoapify.com/ and www.openuv.io
  #will need to pick apart form data, determine if you have city, state and country or just city and country
  #save a boolean (has_state) for if you have city, state, and country for True and then if just city and country False
  #save those fields in variables
  #if has_state construct url for get_coordinates differently than if has_state is False
  #execute get_coordinates save result in var
  # execute get_uv_index put in get_coordinates var as param save in var
  #return var for results of get_uv_index (can simplify after testing by just returning get_uv_index execution)



  #then construct

#if __name__ == "__main__":
  #process_location() #insert fake form_data for testing
