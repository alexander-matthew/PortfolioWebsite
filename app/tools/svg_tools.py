from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
from pathlib import Path
import math
from abc import ABC, abstractmethod


class SVGError(Exception):
    """Base exception class for SVG-related errors"""
    pass


class ValidationError(SVGError):
    """Raised when invalid parameters are provided"""
    pass


@dataclass
class Style:
    fill: str = "none"
    stroke: str = "black"
    stroke_width: float = 1
    opacity: float = 1

    def __post_init__(self):
        self._validate_color(self.fill)
        self._validate_color(self.stroke)
        self._validate_numeric_range(self.opacity, 0, 1, "opacity")
        self._validate_positive(self.stroke_width, "stroke_width")

    @staticmethod
    def _validate_color(color: str):
        if color == "none":
            return

        # Check if it's a valid color name
        if color in VALID_COLOR_NAMES:
            return

        # Check hex format
        if color.startswith("#"):
            if len(color) in [4, 7, 9]:  # #RGB, #RRGGBB, #RRGGBBAA
                return

        # Check rgb/rgba format
        if color.startswith("rgb"):
            return

        # Check hsl/hsla format
        if color.startswith("hsl"):
            return

        raise ValidationError(f"Invalid color format: {color}")

    @staticmethod
    def _validate_numeric_range(value: float, min_val: float, max_val: float, param_name: str):
        if not min_val <= value <= max_val:
            raise ValidationError(f"{param_name} must be between {min_val} and {max_val}")

    @staticmethod
    def _validate_positive(value: float, param_name: str):
        if value < 0:
            raise ValidationError(f"{param_name} must be positive")

    def to_svg_attrs(self) -> str:
        return f'fill="{self.fill}" stroke="{self.stroke}" stroke-width="{self.stroke_width}" opacity="{self.opacity}"'


class Shape(ABC):
    def __init__(self, style: Style):
        self.style = style

    @abstractmethod
    def to_svg(self) -> str:
        pass


class Ellipse(Shape):
    def __init__(self, x: float, y: float, width: float, height: float, rotation: float = 0, style: Style = None):
        super().__init__(style)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self._validate()

    def _validate(self):
        if self.width <= 0 or self.height <= 0:
            raise ValidationError("Ellipse dimensions must be positive")

    def to_svg(self) -> str:
        transform = f' transform="rotate({self.rotation} {self.x} {self.y})"' if self.rotation != 0 else ''
        return f'<ellipse cx="{self.x}" cy="{self.y}" rx="{self.width / 2}" ry="{self.height / 2}" {self.style.to_svg_attrs()}{transform}/>'


class Circle(Ellipse):
    def __init__(self, x: float, y: float, diameter: float, style: Style = None):
        super().__init__(x, y, diameter, diameter, 0, style)


class Rectangle(Shape):
    def __init__(self, x: float, y: float, width: float, height: float, style: Style = None):
        super().__init__(style)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._validate()

    def _validate(self):
        if self.width <= 0 or self.height <= 0:
            raise ValidationError("Rectangle dimensions must be positive")

    def to_svg(self) -> str:
        return f'<rect x="{self.x}" y="{self.y}" width="{self.width}" height="{self.height}" {self.style.to_svg_attrs()}/>'


class Canvas:
    def __init__(self, width: int, height: int):
        self._validate_dimensions(width, height)
        self.width = width
        self.height = height
        self.elements: List[Shape] = []
        self.style = Style()
        self.current_shape: List[Tuple[float, float]] = []

    @staticmethod
    def _validate_dimensions(width: int, height: int):
        if width <= 0 or height <= 0:
            raise ValidationError("Canvas dimensions must be positive")
        if width > 16384 or height > 16384:  # Reasonable max size to prevent memory issues
            raise ValidationError("Canvas dimensions too large")

    def background(self, color: str):
        try:
            style = Style(fill=color, stroke="none")
            rect = Rectangle(0, 0, self.width, self.height, style)
            self.elements.insert(0, rect)
        except ValidationError as e:
            raise ValidationError(f"Invalid background color: {str(e)}")

    def fill(self, color: str):
        try:
            self.style = Style(
                fill=color,
                stroke=self.style.stroke,
                stroke_width=self.style.stroke_width,
                opacity=self.style.opacity
            )
        except ValidationError as e:
            raise ValidationError(f"Invalid fill color: {str(e)}")

    def stroke(self, color: str):
        try:
            self.style = Style(
                fill=self.style.fill,
                stroke=color,
                stroke_width=self.style.stroke_width,
                opacity=self.style.opacity
            )
        except ValidationError as e:
            raise ValidationError(f"Invalid stroke color: {str(e)}")

    def circle(self, x: float, y: float, diameter: float) -> Circle:
        circle = Circle(x, y, diameter, self.style)
        self.elements.append(circle)
        return circle

    def ellipse(self, x: float, y: float, width: float, height: float, rotation: float = 0) -> Ellipse:
        ellipse = Ellipse(x, y, width, height, rotation, self.style)
        self.elements.append(ellipse)
        return ellipse

    def begin_shape(self):
        if self.current_shape:
            raise SVGError("Cannot begin shape: Previous shape not ended")
        self.current_shape = []

    def vertex(self, x: float, y: float):
        if not self.current_shape and not isinstance(self.current_shape, list):
            raise SVGError("Cannot add vertex: No shape begun")
        self.current_shape.append((x, y))

    def end_shape(self, close: bool = False):
        if not self.current_shape:
            raise SVGError("Cannot end shape: No shape begun")
        if len(self.current_shape) < 2:
            raise SVGError("Shape must have at least 2 vertices")

        points = " ".join(f"{x},{y}" for x, y in self.current_shape)
        close_path = "Z" if close else ""
        path = f'<path d="M {points} {close_path}" {self.style.to_svg_attrs()}/>'
        self.elements.append(path)
        self.current_shape = []

    def save(self, filename: Union[str, Path]):
        try:
            filepath = Path(filename)
            if filepath.suffix.lower() != '.svg':
                raise ValidationError("Filename must have .svg extension")

            svg_content = self._generate_svg()

            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(svg_content, encoding='utf-8')

        except (OSError, ValidationError) as e:
            raise SVGError(f"Failed to save SVG: {str(e)}")

    def _generate_svg(self) -> str:
        elements_svg = "\n    ".join(
            element.to_svg() if isinstance(element, Shape)
            else str(element)
            for element in self.elements
        )

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
    {elements_svg}
</svg>'''


# Constants
VALID_COLOR_NAMES = {
    "black", "white", "red", "green", "blue", "yellow", "purple", "orange",
    "gray", "darkred", "darkgreen", "darkblue", "none"
}