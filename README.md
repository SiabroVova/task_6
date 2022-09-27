The programm for parsing documents with information about start and end data of drivers, file with abbriviations for drivers and show statistics depends from requested parameters.

Commands:
    general usage with sorting from winner: main.py --files <folders name>
With reversed sort, need to input desc in "--sort" parameter:
    main.py --files <folders name> --sort <asc/desc> 
Statistic for separate deriver:
    main.py --files <folders name> --driver "<driver name>"

To web access to functions please use next commands:
http://localhost:5000/report - shows common statistic
http://localhost:5000/report/drivers/ - shows list of drivers name and code. Code should be a link on info about drivers
http://localhost:5000/report/drivers/SVF - shows info about a drivers SVF is an example
Also, each route could get order parameter:
http://localhost:5000/report/desc - "desc" for reserve sorting and "asc" for simple
http://localhost:5000/report/drivers/desc - "desc" for reserve sorting and "asc" for simple
