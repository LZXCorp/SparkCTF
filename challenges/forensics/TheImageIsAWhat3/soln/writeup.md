# Solution

1. Using the HEX Editor, search for different variations of `1A 45 DF A3`.
2. When searching using the last 3 bytes, we find the file signature is wrong: `25 50 DF A3`
3. Change the first two bytes from `25 50` to `1A 45`.
4. Export the file from the HEX Editor and rename the file extension to `.mkv`.
5. Within the description showed `???Extract`, which is presumed to be the tool we have to use to extract the Flag from.
6. Using MKVExtract to extract the metadata from the `.mkv` video, we get the following output,
```json
{
    ... ,
    "format": {
        "filename": "pressure.mkv",
        "nb_streams": 2,
        "nb_programs": 0,
        "format_name": "matroska,webm",
        "format_long_name": "Matroska / WebM",
        "start_time": "0.067000",
        "duration": "44.167000",
        "size": "1203607",
        "bit_rate": "218010",
        "probe_score": 100,
        "tags": {
            "encoder": "Lavf55.33.100",
            "flag_hidden": "dtrs1opy_qc0_awlyp_dtep"
        }
    }
}
```

7. We find a not so flaggy flag hidden in the metadata. Using a bruteforce Caesar Cipher tool, we find that the flag is actually: `sigh1den_fr0_plane_site`. Which when cleaned up, becomes: `SIG{h1den_fr0_plane_site}`