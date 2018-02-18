def convertOpeningHours(restaurant):
  if restaurant['open24h']:
    return '24/7'
  else:
    # todo: compress opening hours if possible
    return ('Mo ' + restaurant['monday'].replace(' ', '') +
            '; Tu ' + restaurant['tuesday'].replace(' ', '') +
            '; We ' + restaurant['wednesday'].replace(' ', '') +
            '; Th ' + restaurant['thursday'].replace(' ', '') +
            '; Fr ' + restaurant['friday'].replace(' ', '') +
            '; Sa ' + restaurant['saturday'].replace(' ', '') +
            '; Su ' + restaurant['sunday'].replace(' ', ''))
