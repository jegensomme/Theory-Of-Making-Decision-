package ru.jegensomme;

import java.util.ArrayList;
import java.util.HashMap;

public class Util {

    //дискретизация возможных значений остатков
    public static  ArrayList<Double> discretize(double X0, int disc_number) {

        ArrayList<Double> X = new ArrayList<>();
        double step = X0 / disc_number;

        for(int i = 0; i <= disc_number; i++) {
            X.add(step*i);
        }

        return X;
    }

    //приближенное значение остатка к значениям из таблицы возможных остатков
    private static double e_approx(double e, ArrayList<Double> possibleValues) {

        for(int i = 0; i < possibleValues.size(); i++) {

            double diff = e - possibleValues.get(i);

            if(diff < 0) {
                if(Math.abs(e - possibleValues.get(i)) <= Math.abs(e - possibleValues.get(i - 1)))
                    return possibleValues.get(i);
                else
                    return possibleValues.get(i - 1);
            }

            if(diff == 0)
                return possibleValues.get(i);
        }

        return 0;
    }

    //остаток  денежных средств к концу k-го шага
    public static double e(double u, double e_prev) {

        return (0.74*u) + 0.81*(e_prev - u);
    }

    //зависимость производительности цеха N1 от дополнителных вложенных средств x
    public static double g1(double x) {

        return (5 + Math.pow((x + 40), 0.6));
    }

    //зависимость производительности цеха N2 от дополнителных вложенных средств x
    private static double g2(double x) {

        return (7 + Math.pow((x + 20), 0.5));
    }

    //доход на k-м шаге
    public static double f(double e_prev, double u) {

        return g1(u) + g2(e_prev - u);

    }

    //таблица e, S(e[k-1], u(e[k-1])
    public static HashMap<Double, ArrayList<Double>> S_table(HashMap<Double, ArrayList<Double>> S_table_next, ArrayList<Double> X) {

        HashMap<Double, ArrayList<Double>> S_table = new HashMap<>();

        for(int i = 0; i < X.size(); i++) {

            double e_prev = X.get(i);
            ArrayList<Double> S = new ArrayList<>();

            for(int j = 0; j <= i; j++) {
                double ui = X.get(j);
                double Si = f(e_prev, ui);;
                if(S_table_next != null) {
                    double e = e(ui, e_prev);
                    e = e_approx(e, X);
                    double S_next = S_table_next.get(e).get(0);
                    Si += S_next;
                }

                S.add(Si);
            }

            double S_max = S.stream().max(Double::compareTo).get();
            double u = X.get(S.indexOf(S_max));

            ArrayList<Double> SU = new ArrayList<>();
            SU.add(S_max);
            SU.add(u);
            S_table.put(e_prev, SU);
        }

        return S_table;
    }

    //таблица (e[k-1], uk)
    public static ArrayList<ArrayList<Double>> ue_list(double e0, double u1, ArrayList<HashMap<Double, ArrayList<Double>>> S_table_list, ArrayList<Double> X, int n) {

        ArrayList<ArrayList<Double>> ue_list = new ArrayList<>();

        ArrayList<Double> ue = new ArrayList<>();
        ue.add(u1);
        ue.add(e0);
        ue_list.add(ue);

        double u = u1;
        double e_prev = e0;

        for(int i = 1; i >= 0; i--) {

            HashMap<Double, ArrayList<Double>> S_table = S_table_list.get(i);
            double e = e(u, e_prev);
            e = e_approx(e, X);
            double u_next = S_table.get(e).get(1);

            ue = new ArrayList<>();
            ue.add(u_next);
            ue.add(e);
            ue_list.add(ue);

            e_prev = e;
            u = u_next;

        }

        return ue_list;
    }

}
