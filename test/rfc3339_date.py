#!/usr/bin/env python3
# encoding: utf-8

import datetime as dt

def rfc3339_date(dt, utc_z=False):
    """ Output datetime object as RFC 3339 string, an ISO 8601 profile.
        Compatible with W3C-DTF format.
        utc_z=True outputs "Z" instead of "+00:00" for UTC datetimes."""

    if dt.tzinfo is None:
        suffix = "-00:00" # unknown offset, naive dt
    else:
        suffix = dt.strftime("%z")
        suffix = suffix[:-2] + ":" + suffix[-2:]
        if utc_z and suffix == "+00:00":
            suffix = "Z"
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + suffix

d_naive = dt.datetime.now()
d_local = d_naive.astimezone()
d_utc = d_local.astimezone(dt.timezone.utc)

print("--- datetime ---")
print("Naive       :", d_naive)
print("Local       :", d_local)
print("Local as UTC:", d_utc)
print()

print("--- rfc3339_date, utc_z=False ---")
print("Naive       :", rfc3339_date(d_naive))
print("Local       :", rfc3339_date(d_local))
print("Local as UTC:", rfc3339_date(d_utc))
print()

print("--- rfc3339_date, utc_z=True ---")
print("Naive       :", rfc3339_date(d_naive, utc_z=True))
print("Local       :", rfc3339_date(d_local, utc_z=True))
print("Local as UTC:", rfc3339_date(d_utc, utc_z=True))
