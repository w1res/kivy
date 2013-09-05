'''
Action Bar
==========

.. versionadded:: 1.8.0

.. image:: images/actionbar.png
    :align: right

The ActionBar widget is like Android's ActionBar, where items are stacked
horizontally.

The :class:`ActionBar` will contain one :class:`ActionView` and many
:class:`ContextualActionView`\s.
An :class:`ActionView` will contain an :class:`ActionPrevious` having title,
app_icon and previous_icon properties. An :class:`ActionView` will contain
subclasses of :class:`ActionItem`\s. Some predefined ones inlcude an
:class:`ActionButton`, an :class:`ActionToggleButton`, an :class:`ActionCheck`,
an :class:`ActionSeparator` and an :class:`ActionGroup`.

An :class:`ActionGroup` is used to display :class:`ActionItem`\s in a group.
An :class:`ActionView` will always display an :class:`ActionGroup` after other
:class:`ActionItem`\s.
An :class:`ActionView` will contain an :class:`ActionOverflow`.
A :class:`ContextualActionView` is a subclass of an :class:`ActionView`.
'''

__all__ = ('ActionBarException', 'ActionItem', 'ActionButton',
           'ActionToggleButton', 'ActionCheck', 'ActionSeparator',
           'ActionDropDown', 'ActionGroup', 'ActionOverflow',
           'ActionView', 'ContextualActionView', 'ActionPrevious',
           'ActionBar')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, NumericProperty, \
    BooleanProperty, StringProperty, ListProperty, OptionProperty
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from functools import partial
from kivy.config import Config


window_icon = ''
if Config:
    window_icon = Config.get('kivy', 'window_icon')


class ActionBarException(Exception):
    '''ActionBarException class
    '''
    pass


class ActionItem(object):
    '''ActionItem class, an abstract class for all ActionBar widgets. To create
       a custom widget for an ActionBar, inherit from this
       class. See module documentation for more information.
    '''

    minimum_width = NumericProperty('90sp')
    '''Minimum Width required by an ActionItem.

       :data:`minimum_width` is a :class:`~kivy.properties.NumericProperty` and
       defaults to '90sp'.
    '''

    important = BooleanProperty(False)
    '''Determines if an ActionItem is important or not.

       :data:`important` is a :class:`~kivy.properties.BooleanProperty` and
       defaults to False.
    '''

    inside_group = BooleanProperty(False)
    '''(internal) Determines if an ActionItem is displayed inside an
       ActionGroup or not.

       :data:`inside_group` is a :class:`~kivy.properties.BooleanProperty` and
       defaults to False.
    '''

    background_normal = StringProperty(
        'atlas://data/images/defaulttheme/action_item')
    '''Background image of the ActionItem used for the default graphical
       representation when the ActionItem is not pressed.

       :data:`background_normal` is a :class:`~kivy.properties.StringProperty`
       and defaults to 'atlas://data/images/defaulttheme/action_item'.
    '''

    background_down = StringProperty(
        'atlas://data/images/defaulttheme/action_item_down')
    '''Background image of the ActionItem used for default graphical
       representation when an ActionItem is pressed.

       :data:`background_down` is a :class:`~kivy.properties.StringProperty`
       and defaults to 'atlas://data/images/defaulttheme/action_item_down'.
    '''

    mipmap = BooleanProperty(True)
    '''Defines whether the image/icon dispayed on top of the button uses a
    mipmap or not.

    :data:`mipmap` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to `True`.
    '''


class ActionButton(Button, ActionItem):
    '''ActionButton class, see module documentation for more information.

    The text color, width and size_hint_x are set manually via the Kv language
    file. It covers a lot of cases: with/without an icon, with/without a group
    and takes care of the padding between elements.

    You don't have much control over these properties, so if you want to
    customize it's appearance, we suggest you create you own button
    representation. You can do this by creating a class that subclasses an
    existing widget and an :class:`ActionItem`::

        class MyOwnActionButton(Button, ActionItem):
            pass

    You can then create your own style using the Kv language.
    '''

    icon = StringProperty(None, allownone=True)
    '''Source image to use when the Button is part of the ActionBar. If the
    Button is in a group, the text will be preferred.
    '''


class ActionPrevious(ActionButton):
    '''ActionPrevious class, see module documentation for more information.
    '''

    with_previous = BooleanProperty(True)
    '''Specifies whether clicking on ActionPrevious will load the previous
       screen or not. If True, the previous_icon will be shown otherwise it
       will not.

       :data:`with_previous` is a :class:`~kivy.properties.BooleanProperty` and
       defaults to True.
    '''

    app_icon = StringProperty(window_icon)
    '''Application icon for the ActionView.

       :data:`app_icon` is a :class:`~kivy.properties.StringProperty`
       and defaults to the window icon if set, otherwise
       'data/logo/kivy-icon-32.png'.
    '''

    previous_image = StringProperty(
        'atlas://data/images/defaulttheme/previous_normal')
    '''Image for the 'previous' ActionButtons default graphical representation.

       :data:`previous_image` is a :class:`~kivy.properties.StringProperty` and
       defaults to 'atlas://data/images/defaulttheme/previous_normal'.
    '''

    title = StringProperty('')
    '''Title for ActionView.

       :data:`title` is a :class:`~kivy.properties.StringProperty` and
       defaults to ''.
    '''

    def __init__(self, **kwargs):
        super(ActionPrevious, self).__init__(**kwargs)
        if not self.app_icon:
            self.app_icon = 'data/logo/kivy-icon-32.png'


class ActionToggleButton(ActionItem, ToggleButton):
    '''ActionToggleButton class, see module documentation for more information.
    '''

    icon = StringProperty(None, allownone=True)
    '''Source image to use when the Button is part of the ActionBar. If the
    Button is in a group, the text will be preferred.
    '''



class ActionCheck(ActionItem, CheckBox):
    '''ActionCheck class, see module documentation for more information.
    '''
    pass


class ActionSeparator(ActionItem, Widget):
    '''ActionSeparator class, see module documentation for more information.
    '''

    background_image = StringProperty(
        'atlas://data/images/defaulttheme/separator')
    '''Background image for the separators default graphical representation.

       :data:`background_image` is a :class:`~kivy.properties.StringProperty`
       and defaults to 'atlas://data/images/defaulttheme/separator'.
    '''


class ActionDropDown(DropDown):
    '''ActionDropDown class, see module documentation for more information.
    '''
    pass


class ActionGroup(ActionItem, Spinner):
    '''ActionGroup class, see module documentation for more information.
    '''

    use_separator = BooleanProperty(False)
    '''Specifies whether to use a separator after/before this group or not.

       :data:`use_separator` is a :class:`~kivy.properties.BooleanProperty` and
       defaults to False.
    '''

    separator_image = StringProperty(
        'atlas://data/images/defaulttheme/separator')
    '''Background Image for an ActionSeparator in an ActionView.

       :data:`separator_image` is a :class:`~kivy.properties.StringProperty`
       and defaults to 'atlas://data/images/defaulttheme/separator'.
    '''

    separator_width = NumericProperty(0)
    '''Width of the ActionSeparator in an ActionView.

       :data:`separator_width` is a :class:`~kivy.properties.NumericProperty`
       and defaults to 0.
    '''

    mode = OptionProperty('normal', options=('normal', 'spinner'))
    '''Sets the current mode of an ActionGroup. If mode is 'normal', the
       ActionGroups children will be displayed normally if there is enough
       space, otherwise they will be displayed in a spinner. If mode is
       'spinner', then the children will always be displayed in a spinner.

       :data:`mode` is a :class:`~kivy.properties.OptionProperty` and
       defaults to 'normal'.
    '''

    def __init__(self, **kwargs):
        self.list_action_item = []
        self._list_overflow_items = []
        super(ActionGroup, self).__init__(**kwargs)
        self.dropdown_cls = ActionDropDown

    def add_widget(self, item):
        if isinstance(item, ActionSeparator):
            super(ActionGroup, self).add_widget(item)
            return

        if not isinstance(item, ActionItem):
            raise ActionBarException('ActionGroup only accepts ActionItem')

        self.list_action_item.append(item)

    def show_group(self):
        self.clear_widgets()
        for item in self._list_overflow_items + self.list_action_item:
            item.inside_group = True
            self._dropdown.add_widget(item)

    def _build_dropdown(self, *largs):
        if self._dropdown:
            self._dropdown.dismiss()
            self._dropdown = None
        self._dropdown = self.dropdown_cls()

    def _update_dropdown(self, *largs):
        pass

    def _toggle_dropdown(self, *largs):
        self.is_open = not self.is_open
        ddn = self._dropdown
        ddn.size_hint_x = None
        children = ddn.children[0].children
        ddn.width = max([self.width, children[0].minimum_width])
        for item in children:
            item.size_hint_y = None
            item.height = max([self.height, '48sp'])

    def clear_widgets(self):
        self._dropdown.clear_widgets()


class ActionOverflow(ActionGroup):
    '''ActionOverflow class, see module documentation for more information.
    '''

    overflow_image = StringProperty(
        'atlas://data/images/defaulttheme/overflow')
    '''Image to be used as an Overflow Image.

      :data:`overflow_image` is an :class:`~kivy.properties.ObjectProperty` and
       defaults to 'atlas://data/images/defaulttheme/overflow'.
    '''

    def add_widget(self, action_item, index=0):
        if action_item is None:
            return

        if isinstance(action_item, ActionSeparator):
            return

        if not isinstance(action_item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem'
                    ' (got {!r}'.format(action_item))

        else:
            if index == 0:
                index = len(self._list_overflow_items)
            self._list_overflow_items.insert(index, action_item)

    def show_default_items(self, parent):
        # display overflow and it's items if widget's directly added to it
        if self._list_overflow_items == []:
            return
        self.show_group()
        super(parent.__class__, parent).add_widget(self)


class ActionView(BoxLayout):
    '''ActionView class, see module documentation for more information.
    '''

    action_previous = ObjectProperty(None)
    '''Previous button for an ActionView.

       :data:`action_previous` is an :class:`~kivy.properties.ObjectProperty`
        and defaults to None.
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color in the format (r, g, b, a).

       :data:`background_color` is a :class:`~kivy.properties.ListProperty` and
        defaults to [1, 1, 1, 1].
    '''

    background_image = StringProperty(
        'atlas://data/images/defaulttheme/action_view')
    '''Background image of an ActionViews default graphical represenation.

      :data:`background_image` is an :class:`~kivy.properties.StringProperty`
      and defaults to 'atlas://data/images/defaulttheme/action_view'.
    '''

    use_separator = BooleanProperty(False)
    '''Specify whether to use a separator before every ActionGroup or not.

       :data:`use_separator` is a :class:`~kivy.properties.BooleanProperty` and
       defaults to False.
    '''

    overflow_group = ObjectProperty(None)
    '''Widget to be used for the overflow.

       :data:`overflow_group` is an :class:`~kivy.properties.ObjectProperty`
       and defaults to an instance of :class:`ActionOverflow`.
    '''

    def __init__(self, **kwargs):
        self._list_action_items = []
        self._list_action_group = []
        super(ActionView, self).__init__(**kwargs)
        self._state = ''
        self.overflow_group = ActionOverflow(use_separator=self.use_separator)

    def on_action_previous(self, instance, value):
        self._list_action_items.insert(0, value)

    def add_widget(self, action_item, index=0):
        if action_item is None:
            return

        if not isinstance(action_item, ActionItem):
            raise ActionBarException('ActionView only accepts ActionItem'
                    ' (got {!r}'.format(action_item))

        elif isinstance(action_item, ActionOverflow):
            self.overflow_group = action_item
            action_item.use_separator = self.use_separator

        elif isinstance(action_item, ActionGroup):
            self._list_action_group.append(action_item)
            action_item.use_separator = self.use_separator

        elif isinstance(action_item, ActionPrevious):
            self.action_previous = action_item

        else:
            super(ActionView, self).add_widget(action_item, index)
            if index == 0:
                index = len(self._list_action_items)
            self._list_action_items.insert(index, action_item)

    def on_use_separator(self, instance, value):
        for group in self._list_action_group:
            group.use_separator = value
        self.overflow_group.use_separator = value

    def _clear_all(self):
        self.clear_widgets()
        for group in self._list_action_group:
            group.clear_widgets()

        self.overflow_group.clear_widgets()
        self.overflow_group.list_action_item = []

    def _layout_all(self):
        # all the items can fit to the view, so expand everything
        super_add = super(ActionView, self).add_widget
        self._state = 'all'
        self._clear_all()
        super_add(self.action_previous)
        if len(self._list_action_items) > 1:
            for child in self._list_action_items[1:]:
                child.inside_group = False
                super_add(child)

        for group in self._list_action_group:
            if group.mode == 'spinner':
                super_add(group)
                group.show_group()
            else:
                if group.list_action_item != []:
                    super_add(ActionSeparator())
                for child in group.list_action_item:
                    child.inside_group = False
                    super_add(child)

        self.overflow_group.show_default_items(self)

    def _layout_group(self):
        # layout all the items in order to pack them per group
        super_add = super(ActionView, self).add_widget
        self._state = 'group'
        self._clear_all()
        super_add(self.action_previous)
        if len(self._list_action_items) > 1:
            for child in self._list_action_items[1:]:
                super_add(child)
                child.inside_group = False

        for group in self._list_action_group:
            super_add(group)
            group.show_group()

        self.overflow_group.show_default_items(self)

    def _layout_random(self):
        # layout the items in order to pack all of them grouped, and display
        # only the action items having 'important'
        super_add = super(ActionView, self).add_widget
        self._state = 'random'
        self._clear_all()
        hidden_items = []
        hidden_groups = []
        total_width = 0
        super_add(self.action_previous)

        width = (self.width - self.overflow_group.minimum_width -
                self.action_previous.minimum_width)

        if len(self._list_action_items):
            for child in self._list_action_items[1:]:
                if child.important:
                    if child.minimum_width + total_width < width:
                        super_add(child)
                        child.inside_group = False
                        total_width += child.minimum_width
                    else:
                        hidden_items.append(child)
                else:
                    hidden_items.append(child)

        # if space is left then display ActionItem inside their
        # ActionGroup
        if total_width < self.width:
            for group in self._list_action_group:
                if group.minimum_width + total_width +\
                   group.separator_width < width:
                    super_add(group)
                    group.show_group()
                    total_width += group.minimum_width +\
                                   group.separator_width

                else:
                    hidden_groups.append(group)

        group_index = len(self.children) - 1
        # if space is left then display other ActionItems
        if total_width < self.width:
            for child in hidden_items[:]:
                if child.minimum_width + total_width < width:
                    super_add(child, group_index)
                    total_width += child.minimum_width
                    child.inside_group = False
                    hidden_items.remove(child)

        # for all the remaining ActionItems and ActionItems with in
        # ActionGroups, Display them inside overflow_group
        extend_hidden = hidden_items.extend
        for group in hidden_groups:
            extend_hidden(group.list_action_item)

        overflow_group = self.overflow_group

        if hidden_items != []:
            over_add = super(overflow_group.__class__,
                             overflow_group).add_widget
            for child in hidden_items:
                over_add(child)

            overflow_group.show_group()
            super_add(overflow_group)

    def on_width(self, width, *args):
        # determine the layout to use

        # can we display all of them?
        total_width = 0
        for child in self._list_action_items:
            total_width += child.minimum_width
        for group in self._list_action_group:
            for child in group.list_action_item:
                total_width += child.minimum_width
        if total_width <= self.width:
            if self._state != 'all':
                self._layout_all()
            return

        # can we display them per group?
        total_width = 0
        for child in self._list_action_items:
            total_width += child.minimum_width
        for group in self._list_action_group:
            total_width += group.minimum_width
        if total_width < self.width:
            # ok, we can display all the items grouped
            if self._state != 'group':
                self._layout_group()
            return

        # none of the solutions worked, display them in pack mode
        self._layout_random()


class ContextualActionView(ActionView):
    '''ContextualActionView class, see module documentation
       for more information.
    '''
    pass


class ActionBar(BoxLayout):
    '''ActionBar, see module documentation for more information.

    :Events:
        `on_previous`
            Fired when action_previous of action_view is pressed.
    '''

    action_view = ObjectProperty(None)
    '''action_view of ActionBar.

       :data:`action_view` is an :class:`~kivy.properties.ObjectProperty`,
       default to an instance of ActionView.
    '''

    background_color = ListProperty([1, 1, 1, 1])
    '''Background color, in the format (r, g, b, a).

       :data:`background_color` is a :class:`~kivy.properties.ListProperty`,
        default to [1, 1, 1, 1].
    '''

    background_image = StringProperty(
        'atlas://data/images/defaulttheme/action_bar')

    '''Background image of ActionBar for default graphical represenation.

      :data:`background_image` is an :class:`~kivy.properties.StringProperty`,
      default to 'action_bar'
    '''

    border = ListProperty([2, 2, 2, 2])
    ''':data:`border` to be applied to the :data:`background_image`
    '''

    __events__ = ('on_previous',)

    def __init__(self, **kwargs):
        super(ActionBar, self).__init__(**kwargs)
        self._stack_cont_action_view = []
        self._emit_previous = partial(self.dispatch, 'on_previous')

    def add_widget(self, view):
        if isinstance(view, ContextualActionView):
            self._stack_cont_action_view.append(view)
            if view.action_previous is not None:
                view.action_previous.unbind(on_release=self._emit_previous)
                view.action_previous.bind(on_release=self._emit_previous)
            self.clear_widgets()
            super(ActionBar, self).add_widget(view)

        elif isinstance(view, ActionView):
            self.action_view = view
            super(ActionBar, self).add_widget(view)

        else:
            raise ActionBarException(
                'ActionBar can only add ContextualActionView or ActionView')

    def on_previous(self, *args):
        self._pop_contextual_action_view()

    def _pop_contextual_action_view(self):
        '''Remove the current ContextualActionView and display either the
           previous one or the ActionView
        '''
        self._stack_cont_action_view.pop()
        self.clear_widgets()
        if self._stack_cont_action_view == []:
            super(ActionBar, self).add_widget(self.action_view)
        else:
            super(ActionBar, self).add_widget(self._stack_cont_action_view[-1])


if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.uix.floatlayout import FloatLayout
    from kivy.lang import Builder
    from kivy.factory import Factory

    # XXX clean the first registration done from '__main__' here.
    # otherwise kivy.uix.actionbar.ActionPrevious != __main__.ActionPrevious
    Factory.unregister('ActionPrevious')

    Builder.load_string('''
<MainWindow>:
    ActionBar:
        pos_hint: {'top':1}
        ActionView:
            use_separator: True
            ActionPrevious:
                title: 'Action Bar'
                with_previous: False
            ActionOverflow:
            ActionButton:
                text: 'Btn0'
                icon: 'atlas://data/images/defaulttheme/audio-volume-high'
            ActionButton:
                text: 'Btn1'
            ActionButton:
                text: 'Btn2'
            ActionGroup:
                text: 'Group 2'
                ActionButton:
                    text: 'Btn3'
                ActionButton:
                    text: 'Btn4'
            ActionGroup:
                text: 'Group1'
                ActionButton:
                    text: 'Btn5'
                ActionButton:
                    text: 'Btn6'
                ActionButton:
                    text: 'Btn7'
''')

    class MainWindow(FloatLayout):
        pass

    float_layout = MainWindow()
    runTouchApp(float_layout)
