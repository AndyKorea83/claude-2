# Sample Images

Test images for the trash bin detection PoC, organized by ground-truth class.

| Folder | Description | Expected detection |
|--------|-------------|-------------------|
| `empty/` | Street dumpsters with no visible garbage inside or on top | RED box, label `EMPTY` |
| `full/` | Dumpsters with garbage visible above the rim or lid cannot close | RED box, label `FULL` |
| `critical/` | Severely overfilled — garbage bags piled on the ground around the bin | RED box, label `OVERFILLED` + ORANGE boxes for ground garbage |
| `invalid/` | Out-of-scope bins: warehouse/storage settings, underground/semi-underground cylindrical bins | PURPLE box, label `INVALID` |

## Notes

- Images may contain multiple bins of different classes in a single frame.
- Image quality intentionally varies (lighting, angle, resolution) to simulate CCTV conditions.
- Output annotated images are saved alongside source files as `<name>_detected.jpg`.
