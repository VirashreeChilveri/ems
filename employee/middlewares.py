class RoleMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        # one time configuration and initialization
        # get_response is the object of the fn

    def __call__(self,request):
        # Code to be executed for each request b4 the view(& later middleware) are called

        response=self.get_response(request)    
        '''code to b exe for each req/res after the view is called'''
        return response

    def process_view(self,request,view_func,*view_args,**view_kwargs):

        '''called just b4 django calls the view 
        Return either none or HttpResponse'''

        if request.user.is_authenticated:
            request.role=None
            groups=request.user.groups.all()

            if groups:
                request.role=groups[0].name

    # def process_exception(self, request, exception):
    #     """
    #     Called for the response if exception is raised by view.
    #     Return either none or HttpResponse
    #     """
    #     pass            

    # def process_template_response(self,request,response):
    #     '''
    #         request-HttpRequest object
    #         response-HttpResponse object

    #         return templateresponse

    #         Use this to change the template or context if needed.'''   
    #     pass                 
            


