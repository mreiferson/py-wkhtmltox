cdef extern from "wkhtmltox/pdf.h":
    struct wkhtmltopdf_converter:
        pass
    
    struct wkhtmltopdf_object_settings:
        pass
    
    struct wkhtmltopdf_global_settings:
        pass
    
    bint wkhtmltopdf_init(int use_graphics)
    bint wkhtmltopdf_deinit()
    char *wkhtmltopdf_version()
    
    wkhtmltopdf_global_settings *wkhtmltopdf_create_global_settings()
    wkhtmltopdf_object_settings *wkhtmltopdf_create_object_settings()
    
    bint wkhtmltopdf_set_global_setting(wkhtmltopdf_global_settings *settings, char *name, char *value)
    bint wkhtmltopdf_get_global_setting(wkhtmltopdf_global_settings *settings, char *name, char *value, int vs)
    bint wkhtmltopdf_set_object_setting(wkhtmltopdf_object_settings *settings, char *name, char *value)
    bint wkhtmltopdf_get_object_setting(wkhtmltopdf_object_settings *settings, char *name, char *value, int vs)
    
    wkhtmltopdf_converter *wkhtmltopdf_create_converter(wkhtmltopdf_global_settings *settings)
    void wkhtmltopdf_destroy_converter(wkhtmltopdf_converter *converter)
    
    bint wkhtmltopdf_convert(wkhtmltopdf_converter *converter)
    void wkhtmltopdf_add_object(wkhtmltopdf_converter *converter, wkhtmltopdf_object_settings *setting, char *data)
    
    int wkhtmltopdf_http_error_code(wkhtmltopdf_converter *converter)


cdef extern from "wkhtmltox/image.h":
    struct wkhtmltoimage_global_settings:
        pass
    
    struct wkhtmltoimage_converter:
        pass
    
    bint wkhtmltoimage_init(int use_graphics)
    bint wkhtmltoimage_deinit()
    char *wkhtmltoimage_version()
    
    wkhtmltoimage_global_settings *wkhtmltoimage_create_global_settings()
    
    bint wkhtmltoimage_set_global_setting(wkhtmltoimage_global_settings *settings, char *name, char *value)
    bint wkhtmltoimage_get_global_setting(wkhtmltoimage_global_settings *settings, char *name, char *value, int vs)
    
    wkhtmltoimage_converter *wkhtmltoimage_create_converter(wkhtmltoimage_global_settings *settings, char *data)
    void wkhtmltoimage_destroy_converter(wkhtmltoimage_converter *converter)
    
    bint wkhtmltoimage_convert(wkhtmltoimage_converter *converter)
    
    int wkhtmltoimage_http_error_code(wkhtmltoimage_converter *converter)


cdef int wkhtmltopdf_is_init = 0
cdef int wkhtmltoimage_is_init = 0

cdef class _Pdf:
    cdef wkhtmltopdf_global_settings *_c_global_settings
    cdef bint last_http_error_code
    
    def __cinit__(self):
        global wkhtmltopdf_is_init
        if not wkhtmltopdf_is_init:
            wkhtmltopdf_is_init = wkhtmltopdf_init(0)
        
        self._c_global_settings = wkhtmltopdf_create_global_settings()
    
    def __dealloc__(self):
        pass
        #wkhtmltopdf_deinit();
    
    def version(self):
        return wkhtmltopdf_version();
    
    def set_global_setting(self, char *name, char *value):
        return wkhtmltopdf_set_global_setting(self._c_global_settings, name, value)
    
    def convert(self, pages):
        cdef wkhtmltopdf_converter *c
        cdef wkhtmltopdf_object_settings *os
        
        if not len(pages):
            return False
            
        c = wkhtmltopdf_create_converter(self._c_global_settings)
        
        for page in pages:
            os = wkhtmltopdf_create_object_settings()
            for k, v in page.iteritems():
                wkhtmltopdf_set_object_setting(os, k, v)
            wkhtmltopdf_add_object(c, os, NULL)
        
        ret = wkhtmltopdf_convert(c)
        self.last_http_error_code = wkhtmltopdf_http_error_code(c)
        wkhtmltopdf_destroy_converter(c)
        return ret
    
    def http_error_code(self):
        return self.last_http_error_code


class Pdf:
    pages = []
    
    def __init__(self):
        self._pdf = _Pdf()
        self.pages = []
    
    def add_page(self, settings):
        self.pages.append(settings)
    
    def convert(self):
        self._pdf.convert(self.pages)
    
    def __getattr__(self, name):
        return getattr(self._pdf, name)


cdef class Image:
    cdef wkhtmltoimage_global_settings *_c_global_settings
    cdef bint last_http_error_code
    
    def __cinit__(self):
        global wkhtmltoimage_is_init
        if not wkhtmltoimage_is_init:
            wkhtmltoimage_is_init = wkhtmltoimage_init(0)
        
        self._c_global_settings = wkhtmltoimage_create_global_settings()
    
    def __dealloc__(self):
        pass
        #wkhtmltoimage_deinit();
    
    def version(self):
        return wkhtmltopdf_version();
    
    def set_global_setting(self, char *name, char *value):
        return wkhtmltoimage_set_global_setting(self._c_global_settings, name, value)
    
    def convert(self):
        cdef wkhtmltoimage_converter *c
        c = wkhtmltoimage_create_converter(self._c_global_settings, NULL)
        ret = wkhtmltoimage_convert(c)
        self.last_http_error_code = wkhtmltoimage_http_error_code(c)
        wkhtmltoimage_destroy_converter(c)
        return ret
    
    def http_error_code(self):
        return self.last_http_error_code
