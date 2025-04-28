# outputs.tf

output "pubsub_topic" {
  value = google_pubsub_topic.spotify_topic.name
}

output "bigquery_table" {
  value = "${google_bigquery_dataset.spotify_dataset.dataset_id}.${google_bigquery_table.spotify_table.table_id}"
}

output "cloud_function_url" {
  value = google_cloudfunctions_function.spotify_function.https_trigger_url
}
