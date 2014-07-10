#pragma pack(2)

typedef struct header_list_ {
char header_title[20];
    int ndata;
    int nchan;
    float dummy;
} header_list, *p_header_list;

typedef struct data_list_ {
    float obs;
    float error;
} data_list, *p_data_list;

typedef struct mean_type_ {
    long double total;
    long double n;
} mean_type, *p_mean_type;

typedef struct stddev_type_ {
    long double n;
    long double delta;
    long double mean;
    long double M2;
} stddev_type, *p_stddev_type;

#pragma pack()
