import tensorflow as tf

import numpy as np
from tfkalman import filters


class KalmanTest(tf.test.TestCase):

    def createKF(self):
        x = np.array([[8.],
                      [4.]])
        A = np.array([[0.5, 1.5],
                      [1.0, 2.0]])
        B = np.array([[0.5, 1],
                      [1, 3]])
        P = np.array([[1, 1.5],
                      [0.25, 1.25]])
        Q = np.array([[1, 1],
                      [1, 1]])
        H = np.array([[0.5, 1.5],
                      [1.0, 2.0],
                      [3.0, 1.0]])
        kf = filters.KalmanFilter(x=x, A=A, B=B, P=P, Q=Q, H=H)
        return kf

    def testPredict(self):

        kf = self.createKF()
        predict = kf.predict()
        with self.test_session() as sess:
            tf.global_variables_initializer().run()

            u = np.array([[8.],
                          [16.]])

            x_pred, P_pred = sess.run(predict, feed_dict={kf.u:u})

            self.assertAllEqual(x_pred, np.array([[30.],
                                                  [72.]]))
            self.assertAllEqual(P_pred, np.array([[5.375, 7.125],
                                                  [7.75, 10.5]]))
            x_pred1, P_pred1 = sess.run(predict, feed_dict={kf.u:u})
            self.assertAllEqual(x_pred1, np.array([[143.],
                                                   [230.]]))

    def testCorrect(self):

        kf = self.createKF()
        correct = kf.correct()
        with self.test_session() as sess:
            tf.global_variables_initializer().run()

            z = np.array([[8.],
                          [16.],
                          [4.]])
            R = np.array([[0.5, 0.25, 0.75],
                          [0.0, 0.25, 0.5],
                          [0.75, 0.25, 0.5]])

            K, x, P = sess.run(correct, feed_dict={kf.z:z, kf.R:R})

            self.assertAllClose(K, np.array([[-0.583334, 0.166667, 0.40625],
                                             [0.583333, 0.333333, -0.28125]]))
            self.assertAllClose(x, np.array([[-0.583336],
                                             [9.583332]]))
            self.assertAllClose(P, np.array([[0.190103, 1.278644],
                                             [1.153646, 1.502604]]))

if __name__ == "__main__":
    tf.test.main()
