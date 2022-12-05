from dataclasses import dataclass
from typing import Any

@dataclass
class PlotOptions:
    COLORCODE = {
        "red":      '#ee0000', 
        "green":    '#00ee00', 
        "blue":     '#0000ee', 
        "cyan":     '#00eeee', 
        "magenta":  '#ee00ee', 
        "yellow":   '#eeee00', 
        "black":    '#000000', 
        "gray":     '#888888', 
        "darkgray": '#444444', 
        "lightgray":'#bbbbbb', 
        "brown":    '#964b00',
        "lime":     '#bfff00', 
        "olive":    '#808000', 
        "orange":   '#ffa500', 
        "pink":     '#ff69b4', 
        "purple":   '#b300b3', 
        "teal":     '#009a9a', 
        "violet":   '#ee82ee',
        "white":    '#eeeeee'
    }

    """The options class is an object that holds the options for drawing, such as color of line and width of line etc"""
    color: str = "black"
    width: float = 1
    opacity: float = 1

    @property
    def pltcolor(self):
        # return PlotOptions.COLORS[self.color]
        return self.color

    def to_tikz(self) -> str:
        ls_options: list[str] = []
        if self.color:
            ls_options.append(f"color={self.color}")
        if self.width != 1:
            ls_options.append(f"line width={self.width * 0.4}pt")
        if self.opacity:
            ls_options.append(f"draw opacity={self.opacity}")
        return ", ".join(ls_options)
    
    def __copy__(self):
        return PlotOptions(self.color, self.width, self.opacity)