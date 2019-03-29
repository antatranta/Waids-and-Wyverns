"""Utilities for GUI related actions."""


def draw_text(screen, font, text, pos, color=(0, 0, 0), *,
              background=None, center=False, split_char='\n'):
    """
    Draw text to screen.

    :param screen: Screen to draw text too.
    :param font: Font to use.
    :param text: Text to draw.
    :param pos: Position to draw text too.
    :param color: Color of the font.
    :param background: Color of the background.
    :param center: True if text should be centerd.
    :param split_char: Newline character.
    """
    # pylint: disable=invalid-name,too-many-locals
    x, y = pos
    max_width, total_height = (0, 0)

    for line in text.split(split_char):
        width, height = font.size(line)
        max_width = max(max_width, width)
        total_height += height

        surface = font.render(line, True, color, background)

        if center:
            screen.blit(surface, (x - int(width / 2), int(y - height / 2)))
        else:
            screen.blit(surface, (x, y))

        y += int(height)

    return (max_width, total_height)
