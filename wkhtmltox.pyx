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


cdef class Wkpdf:
    cdef wkhtmltopdf_global_settings *_c_global_settings
    
    def __cinit__(self):
        wkhtmltopdf_init(0)
        self._c_global_settings = wkhtmltopdf_create_global_settings()
        
    def set_global_setting(self, char *name, char *value):
        return wkhtmltopdf_set_global_setting(self._c_global_settings, name, value)