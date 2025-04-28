# main.tf

provider "google" {
  project = var.project_id
  region  = var.region
}

# Pub/Sub Topic
resource "google_pubsub_topic" "spotify_topic" {
  name = var.pubsub_topic
}

# BigQuery Dataset
resource "google_bigquery_dataset" "spotify_dataset" {
  dataset_id                  = var.dataset_id
  location                    = var.region
  delete_contents_on_destroy  = true
}

# BigQuery Table
resource "google_bigquery_table" "spotify_table" {
  dataset_id = google_bigquery_dataset.spotify_dataset.dataset_id
  table_id   = var.table_id
  deletion_protection = false

  schema = jsonencode([
    {
      name = "ts"
      type = "TIMESTAMP"
      mode = "REQUIRED"
    },
    {
      name = "artist"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "track"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      name = "ms_played"
      type = "INTEGER"
      mode = "NULLABLE"
    },
    {
      name = "raw_event"
      type = "STRING"
      mode = "NULLABLE"
    }
  ])

  time_partitioning {
    type = "DAY"
    field = "ts"
  }
}

# Cloud Function placeholder
resource "google_storage_bucket" "function_bucket" {
  name                        = "${var.project_id}-spotify-functions"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "function_zip" {
  name   = "spotify_function_source.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = "cloud_function.zip"
}

resource "google_cloudfunctions_function" "spotify_function" {
  name        = "spotify-poller"
  runtime     = "python311"
  trigger_http = true

  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_zip.name

  entry_point = "main"  # main.py file function (later)

  available_memory_mb = 256

  environment_variables = {
    PUBSUB_TOPIC = google_pubsub_topic.spotify_topic.name
    GCP_PROJECT  = var.project_id
    SPOTIFY_ACCESS_TOKEN = "your-spotify-access-token-here"
}

  depends_on = [
    google_storage_bucket_object.function_zip
  ]
}
