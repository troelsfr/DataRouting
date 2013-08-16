import selector as se
import copy


class Router(object):
    
    def __init__(self, routes):
        self.routes = routes
        route_list = []

        for route in routes:            
            route["selector"] = se.compile( route["selector"] )
            route_list.append( (route["priority"], route ) )

        self.route_list = sorted( route_list )
            

    def apply(self, directory):
        for _, route in self.route_list:
            rets =route['selector'].search( directory )
            fnc = route['method']

            for group in rets.groups():
                paths = []
                groups = None
                justadded = []

                for path, kwargs in group:
                    paths.append(path)
                    if groups == None: 
                        groups = kwargs
                    else:
                        for key, val in kwargs.iteritems():
                            if groups[key] != val:
                                if not key in justadded: 
                                    groups[key] = [ groups[key] ] 
                                    justadded.append(key)
                                if not val in groups[key]:
                                    groups[key].append( val )
                for key in justadded:
                    groups[key] = sorted(groups[key])
                qq = copy.copy( route )
                if 'destination' in qq:
                    qq['destination'] = qq['destination'].format( **groups )
                else:
                    qq['destination'] = ''
                fnc(qq , paths, qq['destination'],  **groups )


if __name__ == "__main__":
    def test(route, source, destination = "blah", **kwargs ):
        print source
        print destination
        print "Hello", kwargs

    routes = [
        {
            'name': 'sa_sweep_tables',
            'priority':500,
            'selector' : 'type<::any/id<::all/subs<::all',
            'method' : test,    
            'destination': '{type}/{id[0]}'
            },
        {
            'name': 'other_route',
            'priority':250,
            'selector' : 'type<::any/lst<::all/hello world/::any:\d+',
            'method' : test,            
            }
        ]

    router = Router(routes)
    
    router.apply(".")
