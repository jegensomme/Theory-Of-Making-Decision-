package ru.jegensomme;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        System.out.print("X0: ");
        double X0 = scanner.nextDouble();
        System.out.print("number of months: ");
        int n = scanner.nextInt();
        System.out.print("number of discretion: ");
        int discNumber = scanner.nextInt();

        ArrayList<Double> X = Util.discretize(X0, discNumber);

        long startTime = System.currentTimeMillis();

        ArrayList<HashMap<Double, ArrayList<Double>>> S_table_list = new ArrayList<>();//таблицы e, S(e[k-1]), u(e[k-1])

        HashMap<Double, ArrayList<Double>> S_table_n = Util.S_table(null, X);
        S_table_list.add(S_table_n);

        for (int i = 1; i < n; i++) {
            HashMap<Double, ArrayList<Double>> S_table_next = S_table_list.get(i-1);
            HashMap<Double, ArrayList<Double>> S_table_k = Util.S_table(S_table_next, X);
            S_table_list.add(S_table_k);
        }

        HashMap<Double, ArrayList<Double>> S_table_1 = S_table_list.get(n-1);
        double e0 = X0;
        double u1 = S_table_1.get(e0).get(1);
        ArrayList<ArrayList<Double>>  ue_list = Util.ue_list(e0, u1, S_table_list, X, n);

        for(int i = 0; i < n; i++) {

            System.out.println("S" + (n-i) + "(e[" + (n-i-1) + "])");
            HashMap<Double, ArrayList<Double>> S_table_i = S_table_list.get(i);

            S_table_i.entrySet().forEach(entry -> {
                double e = Math.round(entry.getKey()*10);
                e = e/10;
                ArrayList<Double> SU = entry.getValue();
                double S = Math.round(SU.get(0)*10);
                S = S/10;
                double u = Math.round(SU.get(1)*10);
                u = u/10;
                System.out.println("e = " + e + "     S = " + S + "     u = " + u);
            });

        }

        System.out.println("Result:");
        for(int i = 0; i < ue_list.size(); i++) {
            double u = ue_list.get(i).get(0);
            double e = ue_list.get(i).get(1);
            u = Math.round(u*10);
            e = Math.round(e*10);
            u = u / 10;
            e = e / 10;
            double S = Math.round(Util.f(e, u) * 10);
            S = S / 10;
            System.out.print(i + 1 + " month: ");
            System.out.println("u = " + u + "; e = " + e);
            System.out.println("S = " + S);
        }

        long totalTime = System.currentTimeMillis() - startTime;
        System.out.println("\nExecution time: " + totalTime + " ms");

    }
}
