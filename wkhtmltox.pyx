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


cdef class Pdf:
    cdef wkhtmltopdf_global_settings *_c_global_settings
    cdef wkhtmltopdf_object_settings *_c_object_settings
    cdef bint last_http_error_code
    
    def __cinit__(self):
        wkhtmltopdf_init(0)
        self._c_global_settings = wkhtmltopdf_create_global_settings()
        self._c_object_settings = wkhtmltopdf_create_object_settings()
    
    def __dealloc__(self):
        wkhtmltopdf_deinit();
    
    def version(self):
        return wkhtmltopdf_version();
    
    def set_global_setting(self, char *name, char *value):
        return wkhtmltopdf_set_global_setting(self._c_global_settings, name, value)
    
    def set_object_setting(self, char *name, char *value):
        return wkhtmltopdf_set_object_setting(self._c_object_settings, name, value)
    
    def convert(self):
        cdef wkhtmltopdf_converter *c
        c = wkhtmltopdf_create_converter(self._c_global_settings)
        wkhtmltopdf_add_object(c, self._c_object_settings, NULL)
        ret = wkhtmltopdf_convert(c)
        self.last_http_error_code = wkhtmltopdf_http_error_code(c)
        wkhtmltopdf_destroy_converter(c)
        return ret
    
    def http_error_code(self):
        return self.last_http_error_code


cdef class Image:
    cdef wkhtmltoimage_global_settings *_c_global_settings
    cdef bint last_http_error_code
    
    def __cinit__(self):
        wkhtmltoimage_init(0)
        self._c_global_settings = wkhtmltoimage_create_global_settings()
    
    def __dealloc__(self):
        wkhtmltoimage_deinit();
    
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