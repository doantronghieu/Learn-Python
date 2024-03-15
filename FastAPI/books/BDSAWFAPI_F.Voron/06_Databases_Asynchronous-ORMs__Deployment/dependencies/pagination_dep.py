from fastapi import Query

class Pagination:
  def __init__(self,  maximum_limit: int = 100) -> None:
    self.maximum_limit = maximum_limit

  async def __call__(
      self,
      skip: int = Query(0, ge=0),
      limit: int = Query(10, ge=0),
  ) -> tuple[int, int]:
    # `call` pulls the maximum limit from class properties set at object init
    capped_limit = min(self.maximum_limit, limit)
    return (skip, capped_limit)
  
  async def skip_limit(
    self,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
  ) -> tuple[int, int]:
    capped_limit = min(self.maximum_limit, limit)
    return (skip, capped_limit)

  async def page_size(
    self,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=0),
  ) -> tuple[int, int]:
    capped_size = min(self.maximum_limit, size)
    return (page, capped_size)


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
  # Function dependency to retrieve pagination query parameter
  # Define query integers parameters on endpoint with default values
  # Return values as tuple.
  # Can do more complex things in dependencies
  capped_limit = min(100, limit)
  return skip, capped_limit
