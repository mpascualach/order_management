def should_check_order_database(query_str) -> bool:
  """
  Determine whether the database should be checked for orders based on the user's query.
    
  Args:
  query (str): The user's input query
  
  Returns:
  bool: True if the database should be checked, False otherwise
  """

  query = query.lower()

  order_related_keywords = [
    'order', 'status', 'item', 'measurement', 'date', 'amount',
    'customer', 'pdf', 'csv', 'download', 'history', 'table'
  ]

  if any(keyword in query for keyword in order_related_keywords):
    return True
  
  order_related_patterns = [
    'what is the status of', 'show me', 'get', 'retrieve', 'find',
    'when was', 'how much', 'where is', 'can i see', 'download'
  ]
  if any(pattern in query for pattern in order_related_patterns):
    return True
  
  order_actions = ['create', 'update', 'cancel', 'track']
  if any(action in query for action in order_actions):
    return True
  
  # If none of the above conditions are met, assume no order database check is needed
  return False