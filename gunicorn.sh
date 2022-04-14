#!/urs/bin/env bash

# The default amount of workers is set to 1, determined by the
# WEB_CONCURRENCY env variable.
# Gunicorn advices to use: 2 x $num_proc + 1
# https://docs.gunicorn.org/en/stable/settings.html#workers
# Allow the value to be overridden with env var
if [[ -z "$WEB_CONCURRENCY" ]] || [[ $((WEB_CONCURRENCY)) -lt 1 ]]; then
    WEB_CONCURRENCY=$((`nproc` + 1))
fi

# Increase the default timeout a bit, so we will not get timeouts for
# long calls. All calls are synchrounous, but should be pretty instant
# Rather not increase the timeout, but instead add (better) caching.
TIME_OUT=${TIME_OUT:-30}

# The default worker type is sync. When reading the docs from gunicorn,
# You'll end up using a async worker pretty quickly. However the amount of
# load for this app is very limited.
# Also, all requests are synchronous, so no real need for the async worker
# see: https://hackernoon.com/why-you-should-almost-always-choose-sync-gunicorn-over-workers-ze9c32wj
# When we start experiencing a lot of TIME_OUT's in Sentry, we might need to revisit
# this choice.
# We can fix a lot with additional caching, if required:
# https://pypi.org/project/gunicorn_cache/
WORKER_CLASS=sync

echo Number of workers set: $WEB_CONCURRENCY
echo Timeout set: $TIME_OUT
echo Using worker class: $WORKER_CLASS

# start the process, but allow additional settings to be passed to the script
# output all logging to stdout, so we can collect it with CloudWatch
gunicorn \
    --log-file=- \
    --timeout=$TIME_OUT \
    --preload \
    --workers=$WEB_CONCURRENCY \
    --worker-class=$WORKER_CLASS \
    $*
