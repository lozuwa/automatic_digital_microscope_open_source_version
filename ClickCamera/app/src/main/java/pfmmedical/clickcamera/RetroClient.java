package pfmmedical.clickcamera;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class RetroClient {
    /**
     * URL of the upload folder
     */
    private static final String ROOT_URL = "http://192.168.3.216:5000/";

    public RetroClient() {
    }

    /**
     * Get Retro Client
     * @return JSON Object
     */
    private static Retrofit getRetroClient() {
        return new Retrofit.Builder()
                .baseUrl(ROOT_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
    }

    public static ApiService getApiService() {
        return getRetroClient().create(ApiService.class);
    }
}
