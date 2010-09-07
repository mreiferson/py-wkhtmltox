cdef extern from "wkhtmltox/pdf.h":
    struct wkhtmltopdf_converter:
        pass
    
    struct wkhtmltopdf_object_settings:
        pass
    
    struct wkhtmltopdf_global_settings:
        pass
    
    bint wkhtmltopdf_init(int use_graphics)
    
    wkhtmltopdf_global_settings *wkhtmltopdf_create_global_settings()
    wkhtmltopdf_object_settings *wkhtmltopdf_create_object_settings()
    
    bint wkhtmltopdf_set_global_setting(wkhtmltopdf_global_settings *settings, char *name, char *value)
    bint wkhtmltopdf_get_global_setting(wkhtmltopdf_global_settings *settings, char *name, char *value, int vs)
    bint wkhtmltopdf_set_object_setting(wkhtmltopdf_object_settings *settings, char *name, char *value)
    bint wkhtmltopdf_get_object_setting(wkhtmltopdf_object_settings *settings, char *name, char *value, int vs)
    
    wkhtmltopdf_converter *wkhtmltopdf_create_converter(wkhtmltopdf_global_settings *settings)
    void wkhtmltopdf_destroy_converter(wkhtmltopdf_converter *converter)
    
    int wkhtmltopdf_convert(wkhtmltopdf_converter *converter)
    void wkhtmltopdf_add_object(wkhtmltopdf_converter *converter, wkhtmltopdf_object_settings *setting, char *data)
    
    int wkhtmltopdf_http_error_code(wkhtmltopdf_converter *converter)


cdef class Wkpdf:
    cdef wkhtmltopdf_global_settings *_c_global_settings
    cdef wkhtmltopdf_object_settings *_c_object_settings
    
    def __cinit__(self):
        wkhtmltopdf_init(0)
        self._c_global_settings = wkhtmltopdf_create_global_settings()
        self._c_object_settings = wkhtmltopdf_create_object_settings()
        
    def set_global_setting(self, char *name, char *value):
        return wkhtmltopdf_set_global_setting(self._c_global_settings, name, value)
        
    def set_object_setting(self, char *name, char *value):
        return wkhtmltopdf_set_object_setting(self._c_object_settings, name, value)
    
    def convert(self):
        cdef wkhtmltopdf_converter *c
        c = wkhtmltopdf_create_converter(self._c_global_settings)
        wkhtmltopdf_add_object(c, self._c_object_settings, NULL)
        
        ret = wkhtmltopdf_convert(c)
        
        print "HTTP Error Code: %d" % wkhtmltopdf_http_error_code(c)
        
        wkhtmltopdf_destroy_converter(c)
        
        return ret