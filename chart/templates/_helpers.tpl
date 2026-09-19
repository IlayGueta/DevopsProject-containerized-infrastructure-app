{{/*
Return the full name of the application.
*/}}
{{- define "infrastructure-api.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end }}