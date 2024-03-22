from django import forms
from django.utils.translation import gettext_lazy as _
from schedule.models import Event, Occurrence, Calendar
from schedule.widgets import ColorInput


class SpanForm(forms.ModelForm):
    start = forms.SplitDateTimeField(label=_("start"))
    end = forms.SplitDateTimeField(
        label=_("end"), help_text=_("The end time must be later than start time.")
    )

    def clean(self):
        if "end" in self.cleaned_data and "start" in self.cleaned_data:
            if self.cleaned_data["end"] <= self.cleaned_data["start"]:
                raise forms.ValidationError(
                    _("The end time must be later than start time.")
                )
        return self.cleaned_data


class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    end_recurring_period = forms.DateTimeField(
        label=_("End recurring period"),
        help_text=_("This date is ignored for one time only events."),
        required=False,
    )
    calendars = forms.ModelMultipleChoiceField(queryset=Calendar.objects.all(), required=False, label=_("Calendars"))


    class Meta:
        model = Event
        exclude = ("creator", "created_on", "calendar")

class EventForm(forms.ModelForm):
    start = forms.SplitDateTimeField(label=_("start"))
    end = forms.SplitDateTimeField(
        label=_("end"), help_text=_("The end time must be later than start time.")
    )
    end_recurring_period = forms.DateTimeField(
        label=_("End recurring period"),
        help_text=_("This date is ignored for one time only events."),
        required=False,
    )
    # Add this line to include a field for selecting multiple calendars

    def clean(self):
        cleaned_data = super().clean()
        if "end" in cleaned_data and "start" in cleaned_data:
            if cleaned_data["end"] <= cleaned_data["start"]:
                self.add_error("end", _("The end time must be later than start time."))
        return cleaned_data

    class Meta:
        model = Event
        # Ensure 'calendars' is not in the exclude list
        exclude = ("creator", "created_on")  # 'calendar' is no longer a direct field, so it's removed from exclude
        widgets = {"color_event": ColorInput}


class OccurrenceForm(SpanForm):
    class Meta:
        model = Occurrence
        exclude = ("original_start", "original_end", "event", "cancelled")


class EventAdminForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Event
        widgets = {"color_event": ColorInput}
