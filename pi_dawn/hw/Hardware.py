from pi_dawn.graphics import Color

class Hardware:
    def start_refresh(self):
        pass

    def refresh(self):
        pass

    def set_pixel(self, screen, pixel, color: Color):
        pass
    
    def get_dimensions(self):
        return ()
