import sublime_plugin
import sublime


class ExpandSelectionToLineBefore(sublime_plugin.TextCommand):
    """Expands the current selection region by one line before the selection. On first call if the cursor is not at the beginning of the line, the current line will be selected.

    Consecutive calls continue to expand the selection by another line.

    """

    def find_previous(self, from_point, to_point):
        """Walks backwards to the beginning of the line or one line from a point.

        """

        #find the current line number
        (line, col) = self.view.rowcol(from_point)
        end_point = self.view.line(to_point).end()

        #find the point that corresponds to the beginnning of the line
        line_point = self.view.text_point(line, 0)

        #return if we reached the beginning
        if not line_point > -1:
            return None

        if line_point == from_point:
            #if we are at the beginning of the line the line has been selected already and we select theline before
            start_point = self.view.text_point(line - 1, 0)
        else:
            start_point = line_point

        return start_point, end_point

    def expand_by_line(self, original_region):
        """Returns a new, expanded region to cover the closest function that encloses the given region.

        If there is no enclosing region, the original region is returned.

        """
        search_back_from_point = original_region.begin()
        end_point = original_region.end()

        line_start_point, end_point = self.find_previous(search_back_from_point, end_point)

        total_region = sublime.Region(line_start_point, end_point)
        #scroll the view to show the selection
        self.view.show(line_start_point)

        return total_region

    def run(self, edit):
        sel = self.view.sel()

        new_regions = [self.expand_by_line(region) for region in sel]

        # Don't add to the stack if the selection didn't change.
        # pylint: disable=E0701
        if all(old == new for old, new in zip(sel, new_regions)): return
        # pylint: enable=E0701

        sel.clear()
        for region in new_regions:
            sel.add(region)


class ContractSelectionToLineAfter(sublime_plugin.TextCommand):
    """Walks forward to the next line.

    """

    def find_next(self, from_point, to_point):
        """Walks backwards from a point, until it finds a region that matches
        the given regex.

        Attempts to find the longest match possible. So while "oobar:
        function()" may be a match, this will continue walking backwards until
        it can no longer match, since "foobar: function()" is preferred.

        """

        #find the current line number
        (line, col) = self.view.rowcol(from_point)
        end_point = self.view.line(to_point).end()

        #find the point that corresponds to the beginnning of the line
        line_point = self.view.text_point(line, 0)

        #return if we reached the beginning
        if not line_point > -1:
            return None

        if line_point == from_point:
            #if we are at the beginning of the line the line has been selected already and we select theline after.
            start_point = self.view.text_point(line + 1, 0)
        else:
            start_point = line_point

        return start_point, end_point

    def contract_by_line(self, original_region):
        """Returns a new, expanded region to cover the closest function that encloses the given region.

        If there is no enclosing region, the original region is returned.

        """
        search_back_from_point = original_region.begin()
        end_point = original_region.end()

        line_start_point, end_point = self.find_next(search_back_from_point, end_point)

        total_region = sublime.Region(line_start_point, end_point)
        #scroll the view to show the selection
        self.view.show(line_start_point)

        return total_region

    def run(self, edit):
        sel = self.view.sel()

        new_regions = [self.contract_by_line(region) for region in sel]

        # Don't add to the stack if the selection didn't change.
        # pylint: disable=E0701
        if all(old == new for old, new in zip(sel, new_regions)): return
        # pylint: enable=E0701

        sel.clear()
        for region in new_regions:
            sel.add(region)
