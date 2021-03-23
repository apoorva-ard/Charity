(function () {

    function secondsToTime(sec, colonBlinking) {

        sec = parseInt(sec, 10);

        if (sec <= 0) {
            return '00:00:00';
        }

        var days = Math.floor(sec / 86400);
        var hours = Math.floor((sec - days * 86400) / 3600);
        var minutes = Math.floor((sec - (hours * 3600) - (days * 86400)) / 60);
        var seconds = sec - (days * 86400) - (hours * 3600) - (minutes * 60);

        if (days > 0) { hours += (days * 24); }
        if (hours < 10) { hours = '0' + hours; }
        if (minutes < 10) { minutes = '0' + minutes; }
        if (seconds < 10) { seconds = '0' + seconds; }

        return hours + ':' + minutes + ':' + seconds;
    }

    $.fn.timer = function (ticker, time, callback) {

        if (!window.Ticker || !(ticker instanceof Ticker)) {
            return this;
        }

        var that = this;
        var currTickId = parseInt(this.data('jqTimerInterval'));

        if (currTickId) {
            ticker.clear(currTickId);
        }

        that.html(secondsToTime(time));

        var tickId = ticker.set(function () {
            time--;
            that.html(secondsToTime(time));
            if (time < 0) {
                ticker.clear(tickId);
                if ($.isFunction(callback)) {
                    callback();
                }
            }
        });

        this.data('jqTimerInterval', tickId);
        this.addClass('jq-timer');

        return this;
    };

    $.fn.clearTimers = function () {
        this.find('.jq-timer').each(function () {
            var currInterval = $(this).data('jqTimerInterval');
            if (currInterval) {
                clearInterval(currInterval);
            }
        });
        return this;
    };
})();