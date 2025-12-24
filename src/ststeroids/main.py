from .route import Route
from .route_builder import RouteBuilder
from .router import Router

class StSteroids:
    
    def __init__(self):
        self._router = Router()
        self._routes: dict[str, Route] = {}
        self._default: Route | None = None

    def route(self, name: str) -> "RouteBuilder":
        return RouteBuilder(self, name)

    def default_route(self, target) -> None:
        self._default = Route("__default__", target)

    def register(self, route: "Route"):
        self._routes[route.name] = route
    
    def run(self, entry_route: str | None = None):
        routes = {}

        if self._default:
            routes["__default__"] = self._default
            
        for route in self._routes.values():
            if route.condition:
                if route.condition():
                    routes[route.name] = route
            else:
                routes[route.name] = route

        self._router.register_routes(routes)

        if entry_route:
            self._router.route(entry_route)

        self._router.run()