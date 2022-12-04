from dataclasses import dataclass
from typing import Any

@dataclass
class Options:
    COLORS = {
        "red":      'r', 
        "green":    'g', 
        "blue":     'b', 
        "cyan":     'c', 
        "magenta":  'm', 
        "yellow":   'y', 
        "black":    'k', 
        "gray":     '#888888', 
        "darkgray": '#444444', 
        "lightgray":'#BBBBBB', 
        "brown":    '#964B00',
        "lime":     '#BFFF00', 
        "olive":    '#808000', 
        "orange":   '#ffa500', 
        "pink":     '#ff69b4', 
        "purple":   '#b300b3', 
        "teal":     '#009a9a', 
        "violet":   '#ee82ee',
        "white":    'w'
    }

    """The options class is an object that holds the options for drawing, such as color of line and width of line etc"""
    color: str = ""
    width: float = 1
    opacity: float = 1

    @property
    def pltcolor(self):
        return Options.COLORS[self.color]

    def to_tikz(self) -> str:
        ls_options: list[str] = []
        if self.color:
            ls_options += f"color={self.color}"
        if self.width != 1:
            ls_options += f"line width={self.width * 0.4}pt"
        if self.opacity:
            ls_options += f"draw opacity={self.opacity}"
        return ", ".join(ls_options)
    
    # Create the kwargs thing for plt
    def to_plt(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {}
        if self.color:
            kwargs["color"] = self.pltcolor
        if self.width != 1:
            kwargs["lw"] = self.width
        if self.opacity:
            kwargs["alpha"] = {self.opacity}
        return kwargs