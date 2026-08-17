""" Placing runs of text at absolute pixel positions on a line that Minecraft insists on centring.

A dialog body centres every line on its own total advance, so nothing can be positioned directly. What
can be controlled is the padding around each run, and that is enough: for runs of advance t0..tn placed
at x0..xn, writing p for the pad before each run,

	p[i] = x[i] - x[i-1] - t[i-1]        for i >= 1
	p[0] = 2 * x[0] + sum(p[1:]) + sum(t)

The second line is the whole trick. Padding the front of the line by twice the wanted position cancels
the centring, and the correction terms account for everything drawn after it.
"""
# Imports
from dataclasses import dataclass

from .metrics import FontMetrics


# Classes
@dataclass(frozen=True)
class Run:
	""" One piece of a line: some text, where its left edge belongs, and how it is styled. """
	x: int
	text: str
	color: str = ""
	bold: bool = False


# Functions
class Layout:
	""" Turns runs into the text components a dialog body can hold. """

	@staticmethod
	def pads(runs: list[Run], metrics: FontMetrics) -> list[float]:
		""" Pad to insert before each run so every run lands on its wanted x.

		Examples:
			>>> metrics = FontMetrics({"a": 6.0})
			>>> Layout.pads([Run(x=10, text="a")], metrics)
			[26.0]
		"""
		widths: list[float] = [metrics.advance(run.text, run.bold) for run in runs]
		pads: list[float] = [0.0] * len(runs)
		for index in range(1, len(runs)):
			pads[index] = runs[index].x - runs[index - 1].x - widths[index - 1]
		pads[0] = 2 * runs[0].x + sum(pads[1:]) + sum(widths)
		return pads

	@staticmethod
	def advance(runs: list[Run], metrics: FontMetrics) -> float:
		""" Total advance of a composed line, which is twice the right edge of whichever run is written last.

		It matters because a dialog body wraps any line wider than its `width`, and a wrapped page is a page
		drawn twice, nine pixels apart. Writing the rightmost run first keeps the total small, which is why
		a spread is drawn right page, jump back, left page.
		"""
		last: Run = runs[-1]
		return 2 * (last.x + metrics.advance(last.text, last.bold))

	@staticmethod
	def line(runs: list[Run], metrics: FontMetrics, limit: int) -> list[dict[str, object]]:
		""" Components for one line, alternating an offset run and the text it positions. """
		if not runs:
			return []
		if (width := Layout.advance(runs, metrics)) > limit:
			raise ValueError(f"line advances {width:.0f} past the {limit} pixel body and would wrap: {[run.text for run in runs]}")
		out: list[dict[str, object]] = []
		for run, pad in zip(runs, Layout.pads(runs, metrics), strict=True):
			if (encoded := metrics.offset(int(pad))):
				out.append({"text": encoded})
			component: dict[str, object] = {"text": run.text}
			if run.color:
				component["color"] = run.color
			if run.bold:
				component["bold"] = True
			out.append(component)
		return out

	@staticmethod
	def page(lines: dict[int, list[Run]], metrics: FontMetrics, last_line: int, limit: int) -> list[dict[str, object]]:
		""" Components for a whole page, inserting the blank lines that do the vertical spacing. """
		out: list[dict[str, object]] = []
		for line_number in range(1, last_line + 1):
			if line_number > 1:
				out.append({"text": "\n"})
			out += Layout.line(lines.get(line_number, []), metrics, limit)
		return out
