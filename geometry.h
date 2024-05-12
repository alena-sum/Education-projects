#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

namespace Names {
const double kEpsilon = 1e-5;
const double kInf = 1e9;
}

bool equalityDouble(double first, double second) {
  return (first <= second + Names::kEpsilon && first >= second - Names::kEpsilon);
}

struct Point {
  double x;
  double y;
  Point() {}
  Point(double coord_x, double coord_y) : x(coord_x), y(coord_y) {}

  double getLength(const Point& other) const {
    return sqrt(pow(x - other.x, 2.0) + pow(y - other.y, 2.0));
  }

  Point getTheNearest(Point first, Point second) const {
    if (equalityDouble(getLength(first), getLength(second))) {
      return first;
    }
    if (getLength(first) < getLength(second)) {
      return first;
    }
    return second;
  }

  Point getTheFurthest(Point first, Point second) const {
    if (equalityDouble(getLength(first), getLength(second))) {
      return first;
    }
    if (getLength(first) < getLength(second)) {
      return second;
    }
    return first;
  }

  double getAngleCoefficient(const Point& other) const {
    return (y - other.y) / (x - other.x);
  }
  ~Point() = default;
};

bool operator==(const Point& first, const Point& second) {
  return equalityDouble(first.x, second.x) && equalityDouble(first.y, second.y);
}
bool operator!=(const Point& first, const Point& second) {
  return !(first == second);
}

class Line {
  double x_coefficient_;
  double y_coefficient_;
  double shift_coefficient_ = 1;
 public:
  Line() {}
  Line(double angle_coefficient, double shift) {
    if (shift == 0) {
      shift_coefficient_ = 0;
      y_coefficient_ = -1;
      x_coefficient_ = angle_coefficient;
    } else {
      x_coefficient_ = angle_coefficient / shift;
      y_coefficient_ = -1 / shift;
    }
  }
  Line(Point point, double angle_coefficient) : Line(angle_coefficient, point.y - angle_coefficient * point.x) {}
  Line(Point first, Point second) {
    if (first.x == second.x) {
      if (first.x == 0) {
        shift_coefficient_ = 0;
        y_coefficient_ = 0;
        x_coefficient_ = 1;
      } else {
        y_coefficient_ = 0;
        x_coefficient_ = -1 / first.x;
      }
    } else if ((first.x != 0 && second.y - first.y * (second.x / first.x) == 0) ||
               (second.x != 0 && first.y - second.y * (first.x / second.x) == 0)) {
      Line(first, (first.y - second.y) / (first.x - second.x));
    } else if (first.x != 0) {
      y_coefficient_ = (second.x / first.x - 1) / (second.y - first.y * (second.x / first.x));
      x_coefficient_ = (-1 - y_coefficient_ * first.y) / first.x;
    } else if (second.x != 0) {
      y_coefficient_ = (first.x / second.x - 1) / (first.y - second.y * (first.x / second.x));
      x_coefficient_ = (-1 - y_coefficient_ * first.y) / first.x;
    }
  }

  std::pair<Point, Point> getPointsAtDistance(double length, Point start) const {
    double shift_x;
    double shift_y;
    if (y_coefficient_ != 0) {
      double angle_coef = -x_coefficient_ / y_coefficient_;
      shift_x = length / sqrt(1 + pow(angle_coef, 2.0));
      shift_y = angle_coef * shift_x;
    } else {
      shift_x = 0;
      shift_y = length;
    }
    Point right(start.x + shift_x, start.y + shift_y);
    Point left(start.x - shift_x, start.y - shift_y);
    if (start.y - shift_y < start.y + shift_y && equalityDouble(start.x + shift_x, start.x - shift_x)) {
      return {right, left};
    }
    return {left, right};
  }

  double getAngleCoefficientOfAthwartLine() const {
    if (x_coefficient_ != 0) {
      return y_coefficient_ / x_coefficient_;
    }
    return Names::kInf;
  }

  Point getIntersectionPoint(const Line& other) const {
    double coord_x;
    double coord_y;
    if (y_coefficient_ != 0) {
      coord_x = (other.y_coefficient_ * shift_coefficient_ / y_coefficient_ - other.shift_coefficient_) /
          (other.x_coefficient_ - other.y_coefficient_ * x_coefficient_ / y_coefficient_);
      coord_y = (-x_coefficient_ * coord_x - shift_coefficient_) / y_coefficient_;
      Point needed(coord_x, coord_y);
      return needed;
    }
    coord_x = -shift_coefficient_ / x_coefficient_;
    coord_y = (-other.x_coefficient_ * coord_x - other.shift_coefficient_) / other.y_coefficient_;
    Point needed(coord_x, coord_y);
    return needed;
  }

  bool isParallel(const Line& other) const {
    return (equalityDouble(x_coefficient_ / other.x_coefficient_, y_coefficient_ / other.y_coefficient_) ||
        equalityDouble(other.x_coefficient_ / x_coefficient_, other.y_coefficient_ / y_coefficient_));
  }

  bool containsPoint(const Point& point, const Point& first, const Point& second) const {
    return (equalityDouble(0.0, x_coefficient_ * point.x + y_coefficient_ * point.y + shift_coefficient_)) &&
        (((point.x <= first.x && point.x >= second.x) || (point.x >= first.x && point.x <= second.x))) &&
        ((point.y <= first.y && point.y >= second.y) || (point.y >= first.y && point.y <= second.y));
  }

  friend bool operator==(const Line& first, const Line& second);
  friend bool operator!=(const Line& first, const Line& second);
  friend class Polygon;
  ~Line() = default;
};

bool operator==(const Line& first, const Line& second) {
  return equalityDouble(first.y_coefficient_, second.y_coefficient_) &&
      equalityDouble(first.x_coefficient_, second.x_coefficient_) &&
      equalityDouble(first.shift_coefficient_, second.shift_coefficient_);
}
bool operator!=(const Line& first, const Line& second) {
  return !(first == second);
}

class Shape {
 public:
  virtual std::pair<std::pair<Point, Point>, std::pair<double, double>> isEllipse() const = 0;
  virtual std::vector<Point> isPolygon() const = 0;

  bool operator==(const Shape& another) const {
    std::pair<std::pair<Point, Point>, std::pair<double, double>> fir_ellipse = isEllipse();
    std::pair<std::pair<Point, Point>, std::pair<double, double>> sec_ellipse = another.isEllipse();
    if ((fir_ellipse.second.first == -1 && sec_ellipse.second.first != -1) ||
        (fir_ellipse.second.first != -1 && sec_ellipse.second.first == -1)) {
      return false;
    }
    if (fir_ellipse.second.first != -1) {
      if (equalityDouble(fir_ellipse.second.first, sec_ellipse.second.first) &&
          equalityDouble(fir_ellipse.second.second, sec_ellipse.second.second)) {
        if ((fir_ellipse.first.first == sec_ellipse.first.first && fir_ellipse.first.second == sec_ellipse.first.second) ||
            (fir_ellipse.first.first == sec_ellipse.first.second && fir_ellipse.first.second == sec_ellipse.first.first)) {
          return true;
        }
      }
    } else {
      std::vector<Point> fir_polygon = isPolygon();
      std::vector<Point> sec_polygon = another.isPolygon();
      if (fir_polygon.size() != sec_polygon.size()) {
        return false;
      }
      int size = (int)fir_polygon.size();
      for (int i = 0; i < size; ++i) {
        bool fl = true;
        for (int j = 0; j < size; ++j) {
          if (fir_polygon[(i + j) % size] != sec_polygon[j]) {
            fl = false;
            break;
          }
        }
        if (fl) { return true; }
      }
      std::reverse(sec_polygon.begin(), sec_polygon.end());
      for (int i = 0; i < size; ++i) {
        bool fl = true;
        for (int j = 0; j < size; ++j) {
          if (fir_polygon[(i + j) % size] != sec_polygon[j]) {
            fl = false;
            break;
          }
        }
        if (fl) { return true; }
      }
      return false;
    }
    return false;
  }

  virtual bool isCongruentTo(const Shape& another) const = 0;
  virtual bool isSimilarTo(const Shape& another) const = 0;
  virtual bool containsPoint(const Point& point) const = 0;
  virtual void rotate(const Point& center, double angle) = 0;
  virtual void reflect(const Point& center) = 0;
  virtual void reflect(const Line& axis) = 0;
  virtual void scale(const Point& center, double coefficient) = 0;
  virtual double perimeter() const = 0;
  virtual double area() const = 0;
  friend bool isPolygon(const Shape& shape);
  virtual ~Shape() = default;
};

class Polygon: public Shape {
 private:
  double findSin(Point first, Point second, Point third) const {
    double cos = ((first.x - second.x) * (third.x - second.x) + (first.y - second.y) * (third.y - second.y)) /
        (first.getLength(second) * second.getLength(third));
    return sqrt(1 - pow(cos, 2.0));
  }

  int GetSign(double num) const {
    return (num > 0) - (num < 0);
  }

  bool isIntersectSide(Point first, Point second, Line& ray, Point point) const {
    Line side(first, second);
    if (side == ray || side.isParallel(ray)) {
      return false;
    }
    Point intersect_pnt = side.getIntersectionPoint(ray);
    if (intersect_pnt.x >= point.x && side.containsPoint(intersect_pnt, first, second)) {
      return true;
    }
    return false;
  }

  bool checkForCongruent(std::vector<std::pair<double, double>> sides_first, std::vector<std::pair<double, double>> sides_second, int count_vert) const {
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      for (int j = 0; j < count_vert; ++j) {
        if (!equalityDouble(sides_first[(i + j) % count_vert].first, sides_second[j].first) ||
            !equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[j].second)) {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      for(int j = 0; j < count_vert; ++j) {
        int k = j - 1;
        if (j == 0) { k = count_vert - 1; }
        if (!equalityDouble(sides_first[(i + j) % count_vert].first, sides_second[j].first) ||
            !equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[k].second)) {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      for(int j = 0; j < count_vert; ++j) {
        if (!equalityDouble(sides_first[(i + j) % count_vert].first, sides_second[j].first) ||
            !equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[(j + 1) % count_vert].second)) {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    return false;
  }

  bool checkForSimilar(std::vector<std::pair<double, double>> sides_first, std::vector<std::pair<double, double>> sides_second, int count_vert) const {
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      double ratio = 0;
      for (int j = 0; j < count_vert; ++j) {
        if (equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[j].second)) {
          if (ratio == 0) {
            ratio = sides_first[(i + j) % count_vert].first / sides_second[j].first;
          } else {
            if (!equalityDouble(ratio, sides_first[(i + j) % count_vert].first / sides_second[j].first)) {
              fl = false;
              break;
            }
          }
        } else {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      double ratio = 0;
      for (int j = 0; j < count_vert; ++j) {
        int k = j - 1;
        if (j == 0) { k = count_vert - 1; }
        if (equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[k].second)) {
          if (ratio == 0) {
            ratio = sides_first[(i + j) % count_vert].first / sides_second[j].first;
          } else {
            if (!equalityDouble(ratio, sides_first[(i + j) % count_vert].first / sides_second[j].first)) {
              fl = false;
              break;
            }
          }
        } else {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    for (int i = 0; i < count_vert; ++i) {
      bool fl = true;
      double ratio = 0;
      for (int j = 0; j < count_vert; ++j) {
        if (equalityDouble(sides_first[(i + j) % count_vert].second, sides_second[(j + 1) % count_vert].second)) {
          if (ratio == 0) {
            ratio = sides_first[(i + j) % count_vert].first / sides_second[j].first;
          } else {
            if (!equalityDouble(ratio, sides_first[(i + j) % count_vert].first / sides_second[j].first)) {
              fl = false;
              break;
            }
          }
        } else {
          fl = false;
          break;
        }
      }
      if (fl) { return true; }
    }
    return false;
  }
 protected:
  std::vector<Point> vertices_;
 public:
  Polygon() {}
  Polygon(std::vector<Point> all_vertices) : vertices_(all_vertices) {}
  template<typename First, typename... other>
  void AddPoint(First first, other... second) {
    vertices_.push_back(first);
    AddPoint(second...);
  }
  template<typename First>
  void AddPoint(First first) {
    vertices_.push_back(first);
  }
  template<typename... packet>
  Polygon(packet... arguments) {
    AddPoint(arguments...);
  }

  std::pair<std::pair<Point, Point>, std::pair<double, double>> isEllipse() const override {
    Point first(-Names::kInf, -Names::kInf);
    Point second(-Names::kInf, -Names::kInf);
    return {{first, second}, {-1, -1}};
  }

  std::vector<Point> isPolygon() const override {
    return vertices_;
  }

  int verticesCount() const {
    return (int)vertices_.size();
  }

  double perimeter() const override {
    double result = 0;
    int count_sides = verticesCount();
    for (int i = 0; i < count_sides; ++i) {
      result += vertices_[i % count_sides].getLength(vertices_[(i + 1) % count_sides]);
    }
    return result;
  }

  double area() const override {
    double result = 0.0;
    int count_sides = verticesCount();
    if (count_sides <= 2) { return result; }
    Point first;
    Point second;
    for (int i = 0; i < count_sides; ++i) {
      first = vertices_[i];
      second = vertices_[(i + 1) % count_sides];
      result += first.x * second.y - first.y * second.x;
    }
    return fabs(result) / 2.0;
  }

  void reflect(const Line& axis) override {
    int count_vert = verticesCount();
    for (int i = 0; i < count_vert; ++i) {
      Line perpendicular_axis(vertices_[i], axis.getAngleCoefficientOfAthwartLine());
      Point center = axis.getIntersectionPoint(perpendicular_axis);
      if (vertices_[i] == center) {
        continue ;
      }
      double length = vertices_[i].getLength(center);
      std::pair<Point, Point> search_reflection = perpendicular_axis.getPointsAtDistance(length, center);
      Point reflection = vertices_[i].getTheFurthest(search_reflection.first, search_reflection.second);
      vertices_[i] = reflection;
    }
  }

  void reflect(const Point& center) override {
    int count_vert = verticesCount();
    for (int i = 0; i < count_vert; ++i) {
      if (vertices_[i] == center) {
        continue ;
      }
      Line connecting(vertices_[i], center.getAngleCoefficient(vertices_[i]));
      double length = vertices_[i].getLength(center);
      std::pair<Point, Point> search_reflection = connecting.getPointsAtDistance(length, center);
      Point reflection = vertices_[i].getTheFurthest(search_reflection.first, search_reflection.second);
      vertices_[i] = reflection;
    }
  }

  void rotate(const Point& center, double angle) override {
    int count_vert = verticesCount();
    for (int i = 0; i < count_vert; ++i) {
      if (vertices_[i] == center) {
        continue ;
      }
      double tg_before = vertices_[i].getAngleCoefficient(center);
      double angle_before = atan(tg_before) * 180.0 / M_PI;
      double length = center.getLength(vertices_[i]);
      double tg;
      if (vertices_[i].x == center.x) {
        tg = tan((90 + angle) * M_PI / 180);
      } else {
        tg = tan((angle_before + angle) * M_PI / 180);
      }
      Line now(center, tg);
      std::pair<Point, Point> search_new_point = now.getPointsAtDistance(length, center);
      Point res;
      if (fmod(angle, 360) >= 90 && fmod(angle, 360) <= 270) {
        res = vertices_[i].getTheFurthest(search_new_point.first, search_new_point.second);
      } else {
        res = vertices_[i].getTheNearest(search_new_point.first, search_new_point.second);
      }
      vertices_[i] = res;
    }
  }

  void scale(const Point& center, double coefficient) override {
    if (coefficient == 1.0) {
      return;
    }
    int count_vert = verticesCount();
    for (int i = 0; i < count_vert; ++i) {
      Line connecting(center, vertices_[i].getAngleCoefficient(center));
      double length = fabs(coefficient) * vertices_[i].getLength(center);
      std::pair<Point, Point> search_res = connecting.getPointsAtDistance(length, center);
      Point res;
      if (coefficient > 0) {
        res = vertices_[i].getTheNearest(search_res.first, search_res.second);
      } else {
        res = vertices_[i].getTheFurthest(search_res.first, search_res.second);
      }
      vertices_[i] = res;
    }
  }

  std::vector<Point> getVertices() const {
    return vertices_;
  }

  bool isConvex() const {
    int count_sides = vertices_.size();
    std::vector<Point> assistant(count_sides + 1);
    for (int i = 0; i < count_sides + 1; ++i) {
      assistant[i] = vertices_[i % count_sides];
    }
    for (int i = 0; i < count_sides; ++i) {
      Line cur_side(assistant[i], assistant[i + 1]);
      double x_coef = cur_side.x_coefficient_;
      double y_coef = cur_side.y_coefficient_;
      double shift = cur_side.shift_coefficient_;
      int prev_sign = GetSign(x_coef * vertices_[0].x + y_coef * vertices_[0].y + shift);
      int sign;
      for (int j = 1; i < count_sides; ++i) {
        sign = GetSign(x_coef * vertices_[j].x + y_coef * vertices_[j].y + shift);
        if (!(prev_sign == sign || sign == 0)) {
          return false;
        }
        if (sign != 0) {
          prev_sign = sign;
        }
      }
    }
    return true;
  }

  bool containsPoint(const Point& point) const override {
    int count_vert = verticesCount();
    Line ray(point, 1.567);
    int count = 0;
    for (int i = 0; i < count_vert; ++i) {
      Line side(vertices_[i], vertices_[(i + 1) % count_vert].getAngleCoefficient(vertices_[i]));
      if (side.containsPoint(point, vertices_[i], vertices_[(i + 1) % count_vert])) {
        return true;
      }
      if (isIntersectSide(vertices_[i], vertices_[(i + 1) % count_vert], ray, point)) {
        ++count;
      }
    }
    if (count % 2 == 0) {
      return false;
    }
    return true;
  }

  bool isSimilarTo(const Shape& another) const override {
    std::vector<Point> other = another.isPolygon();
    if (other.size() == 1 || other.size() != vertices_.size()) {
      return false;
    }
    int count_vert = verticesCount();
    std::vector<std::pair<double, double>> sides_first(count_vert);
    std::vector<std::pair<double, double>> sides_second(count_vert);
    for (int i = 0; i < count_vert; ++i) {
      sides_first[i].first = vertices_[i].getLength(vertices_[(i + 1) % count_vert]);
      sides_second[i].first = other[i].getLength(other[(i + 1) % count_vert]);
      sides_first[i].second = findSin(vertices_[i], vertices_[(i + 1) % count_vert], vertices_[(i + 2) % count_vert]);
      sides_second[i].second = findSin(other[i], other[(i + 1) % count_vert], other[(i + 2) % count_vert]);
    }
    if (checkForSimilar(sides_first, sides_second, count_vert)) {
      return true;
    }
    std::reverse(sides_second.begin(), sides_second.end());
    if (checkForSimilar(sides_first, sides_second, count_vert)) {
      return true;
    }
    return false;
  }

  bool isCongruentTo(const Shape& another) const override {
    std::vector<Point> other = another.isPolygon();
    if (other.size() == 1 || other.size() != vertices_.size()) {
      return false;
    }
    int count_vert = verticesCount();
    std::vector<std::pair<double, double>> sides_first(count_vert);
    std::vector<std::pair<double, double>> sides_second(count_vert);
    for (int i = 0; i < count_vert; ++i) {
      sides_first[i].first = vertices_[i].getLength(vertices_[(i + 1) % count_vert]);
      sides_second[i].first = other[i].getLength(other[(i + 1) % count_vert]);
      sides_first[i].second = findSin(vertices_[i], vertices_[(i + 1) % count_vert], vertices_[(i + 2) % count_vert]);
      sides_second[i].second = findSin(other[i], other[(i + 1) % count_vert], other[(i + 2) % count_vert]);
    }
    if (checkForCongruent(sides_first, sides_second, count_vert)) {
      return true;
    }
    std::reverse(sides_second.begin(), sides_second.end());
    if (checkForCongruent(sides_first, sides_second, count_vert)) {
      return true;
    }
    return false;
  }
  ~Polygon() = default;
};

class Ellipse: public Shape {
 protected:
  double big_axle_shaft_;
  double small_axle_shaft_;
  std::pair<Point, Point> focuses_;
 public:
  Ellipse() {}
  Ellipse(Point first_focus, Point second_focus, double length) {
    double center_x = (first_focus.x + second_focus.x) / 2.0;
    double center_y = (first_focus.y + second_focus.y) / 2.0;
    big_axle_shaft_ = length / 2.0;
    double foc_length = sqrt(pow(first_focus.x - center_x, 2.0) + pow(first_focus.y - center_y, 2.0));
    small_axle_shaft_ = sqrt(pow(big_axle_shaft_, 2.0) - pow(foc_length, 2.0));
    focuses_ = {first_focus, second_focus};
  }

  std::vector<Point> isPolygon() const override {
    Point point(-Names::kInf, -Names::kInf);
    std::vector<Point> ans = {point};
    return ans;
  }

  std::pair<std::pair<Point, Point>, std::pair<double, double>> isEllipse() const override {
    return {focuses_, {big_axle_shaft_, small_axle_shaft_}};
  }

  void reflect(const Line& axis) override {
    std::vector<Point> focuses = {focuses_.first, focuses_.second};
    for (int i = 0; i < 2; ++i) {
      Line athwart_axis(focuses[i], axis.getAngleCoefficientOfAthwartLine());
      Point center = axis.getIntersectionPoint(athwart_axis);
      if (focuses[i] == center) {
        continue ;
      }
      double length = focuses[i].getLength(center);
      std::pair<Point, Point> search_reflection = athwart_axis.getPointsAtDistance(length, center);
      Point reflection = focuses[i].getTheFurthest(search_reflection.first, search_reflection.second);
      focuses[i] = reflection;
    }
    focuses_ = {focuses[0], focuses[1]};
  }

  void reflect(const Point& center) override {
    std::vector<Point> focuses = {focuses_.first, focuses_.second};
    for (int i = 0; i < 2; ++i) {
      if (focuses[i] == center) {
        continue ;
      }
      Line connecting(focuses[i], center.getAngleCoefficient(focuses[i]));
      double length = focuses[i].getLength(center);
      std::pair<Point, Point> search_reflection = connecting.getPointsAtDistance(length, center);
      Point reflection = focuses[i].getTheFurthest(search_reflection.first, search_reflection.second);
      focuses[i] = reflection;
    }
    focuses_ = {focuses[0], focuses[1]};
  }

  void rotate(const Point& center, double angle) override {
    std::vector<Point> focuses = {focuses_.first, focuses_.second};
    for (int i = 0; i < 2; ++i) {
      if (focuses[i] == center) {
        continue ;
      }
      double tg_before = focuses[i].getAngleCoefficient(center);
      double angle_before = atan(tg_before) * 180.0 / M_PI;
      double length = center.getLength(focuses[i]);
      double tg;
      if (focuses[i].x == center.x) {
        tg = tan((90 + angle) * M_PI / 180);
      } else {
        tg = tan((angle_before + angle) * M_PI / 180);
      }
      Line now(center, tg);
      std::pair<Point, Point> search_new_point = now.getPointsAtDistance(length, center);
      Point res;
      if (fmod(angle, 360) >= 90 && fmod(angle, 360) <= 270) {
        res = focuses[i].getTheFurthest(search_new_point.first, search_new_point.second);
      } else {
        res = focuses[i].getTheNearest(search_new_point.first, search_new_point.second);
      }
      focuses[i] = res;
    }
    focuses_ = {focuses[0], focuses[1]};
  }

  void scale(const Point& center, double coefficient) override {
    if (coefficient == 1.0) {
      return;
    }
    std::vector<Point> focuses = {focuses_.first, focuses_.second};
    for (int i = 0; i < 2; ++i) {
      Line connecting(center, focuses[i].getAngleCoefficient(center));
      double length = fabs(coefficient) * focuses[i].getLength(center);
      std::pair<Point, Point> search_res = connecting.getPointsAtDistance(length, center);
      Point res;
      if (coefficient > 0) {
        res = focuses[i].getTheNearest(search_res.first, search_res.second);
      } else {
        res = focuses[i].getTheFurthest(search_res.first, search_res.second);
      }
      focuses[i] = res;
    }
    focuses_ = {focuses[0], focuses[1]};
    big_axle_shaft_ *= fabs(coefficient);
    small_axle_shaft_ *= fabs(coefficient);
  }

  double perimeter() const override {
    double result = M_PI * (big_axle_shaft_ + small_axle_shaft_) * (1 + (3 * pow((big_axle_shaft_ - small_axle_shaft_) / (big_axle_shaft_ + small_axle_shaft_), 2.0)) /
                                                                     (10 + sqrt(4 - 3 * pow((big_axle_shaft_ - small_axle_shaft_) / (big_axle_shaft_ + small_axle_shaft_), 2.0))));
    return result;
  }

  double area() const override {
    return M_PI * big_axle_shaft_ * small_axle_shaft_;
  }

  std::pair<Point, Point> focuses() const {
    return focuses_;
  }

  double eccentricity() const {
    return sqrt(1 - pow(small_axle_shaft_ / big_axle_shaft_, 2.0));
  }

  Point center() const {
    double center_x = (focuses_.first.x + focuses_.second.x) / 2.0;
    double center_y = (focuses_.first.y + focuses_.second.y) / 2.0;
    Point cent(center_x, center_y);
    return cent;
  }

  bool containsPoint(const Point& point) const override {
    if (2 * big_axle_shaft_ >= point.getLength(focuses_.first) + point.getLength(focuses_.second)) {
      return true;
    }
    return false;
  }

  bool isCongruentTo(const Shape& another) const override {
    std::pair<std::pair<Point, Point>, std::pair<double, double>> other = another.isEllipse();
    if (other.second.first == -1) { return false; }
    if (equalityDouble(big_axle_shaft_, other.second.first) &&
        equalityDouble(small_axle_shaft_, other.second.second)) {
      return true;
    }
    return false;
  }

  bool isSimilarTo(const Shape& another) const override {
    std::pair<std::pair<Point, Point>, std::pair<double, double>> other = another.isEllipse();
    if (other.second.first == -1) { return false; }
    if (equalityDouble(big_axle_shaft_ / other.second.first, small_axle_shaft_ / other.second.second)) {
      return true;
    }
    return false;
  }

  std::pair<Line, Line> directrices() const {
    double ecc = eccentricity();
    if (focuses_.first.y == focuses_.second.y) {
      Point first(big_axle_shaft_ / ecc, 0);
      Point second(big_axle_shaft_ / ecc, 1);
      Line dir_right(first, second);
      Point third(-big_axle_shaft_ / ecc, 0);
      Point fourth(-big_axle_shaft_ / ecc, 1);
      Line dir_left(third, fourth);
      return {dir_left, dir_right};
    }
    Line foc_line(focuses_.first, focuses_.second);
    Point cent = center();
    std::pair<Point, Point> dir_points = foc_line.getPointsAtDistance(big_axle_shaft_ / ecc, cent);
    Line dir_right(dir_points.second, foc_line.getAngleCoefficientOfAthwartLine());
    Line dir_left(dir_points.first, foc_line.getAngleCoefficientOfAthwartLine());
    return {dir_left, dir_right};
  }
  ~Ellipse() = default;
};

class Circle: public Ellipse {
 public:
  Circle() {}
  Circle(Point cent, double rad) {
    big_axle_shaft_ = rad;
    small_axle_shaft_ = rad;
    focuses_ = {cent, cent};
  }

  double perimeter() const override {
    double rad = big_axle_shaft_;
    return 2.0 * rad * M_PI;
  }

  double radius() const {
    return big_axle_shaft_;
  }
  ~Circle() = default;
};

class Rectangle: public Polygon {
 public:
  Rectangle() {}
  Rectangle(Point first_vert, Point second_vert, double ratio) {
    vertices_.push_back(first_vert);
    double diag = first_vert.getLength(second_vert);
    double small_side;
    double big_side;
    if (ratio >= 1) {
      small_side = diag / sqrt(1 + pow(ratio, 2.0));
      big_side = small_side * ratio;
    } else {
      big_side = diag / sqrt(1 + pow(ratio, 2.0));
      small_side = big_side * ratio;
    }
    double tg_fir = big_side / small_side;
    double tg_sec = small_side / big_side;
    Line diagonal(first_vert, second_vert);
    double tg = first_vert.getAngleCoefficient(second_vert);
    double fir_coef;
    double sec_coef;
    fir_coef = (tg_fir + tg) / (1 - tg_fir * tg);
    sec_coef = (tg - tg_sec) / (1 + tg_sec * tg);
    if ((first_vert.x < second_vert.x && first_vert.y < second_vert.y) ||
        (first_vert.x >= second_vert.x && first_vert.y < second_vert.y)) {
      Line sm_side(first_vert, fir_coef);
      Line bg_side(first_vert, sec_coef);
      std::pair<Point, Point> search_third = sm_side.getPointsAtDistance(small_side, first_vert);
      std::pair<Point, Point> search_fourth = bg_side.getPointsAtDistance(big_side, first_vert);
      Point third_vert = second_vert.getTheNearest(search_third.first, search_third.second);
      Point fourth_vert = second_vert.getTheNearest(search_fourth.first, search_fourth.second);
      vertices_.push_back(third_vert);
      vertices_.push_back(second_vert);
      vertices_.push_back(fourth_vert);
    } else {
      Line sm_side(second_vert, fir_coef);
      Line bg_side(second_vert, sec_coef);
      std::pair<Point, Point> search_third = sm_side.getPointsAtDistance(small_side, second_vert);
      std::pair<Point, Point> search_fourth = bg_side.getPointsAtDistance(big_side, second_vert);
      Point third_vert = first_vert.getTheNearest(search_third.first, search_third.second);
      Point fourth_vert = first_vert.getTheNearest(search_fourth.first, search_fourth.second);
      vertices_.push_back(fourth_vert);
      vertices_.push_back(second_vert);
      vertices_.push_back(third_vert);
    }
  }

  Point center() const {
    double x_cent = (vertices_[0].x + vertices_[2.0].x) / 2.0;
    double y_cent = (vertices_[0].y + vertices_[2.0].y) / 2.0;
    Point cent(x_cent, y_cent);
    return cent;
  }

  std::pair<Line, Line> diagonals() const {
    Line first_diag(vertices_[0], vertices_[2.0]);
    Line second_diag(vertices_[1], vertices_[3]);
    return {first_diag, second_diag};
  }
  ~Rectangle() = default;
};

class Square: public Rectangle {
 public:
  Square() {}
  Square(Point first_vert, Point second_vert) : Rectangle(first_vert, second_vert, 1.0) {}

  Circle circumscribedCircle() const {
    Point cent = center();
    double rad = vertices_[0].getLength(vertices_[1]) / 2.0;
    Circle circ(cent, rad);
    return circ;
  }

  Circle inscribedCircle() const {
    Point cent = center();
    double rad = vertices_[0].getLength(vertices_[1]) / 2.0;
    Circle circ(cent, rad);
    return circ;
  }
  ~Square() = default;
};

class Triangle: public Polygon {
 public:
  Triangle(Point first, Point second, Point third) {
    vertices_ = {first, second, third};
  }

  Line getLine(Point first, Point second) const {
    if (first.x == second.x) {
      Line result(first, second);
      return result;
    }
    Line result(first, second.getAngleCoefficient(first));
    return result;
  }

  Line getHeight(Point first, Point second, Point third) const {
    Line side = getLine(first, third);
    Line height(second, side.getAngleCoefficientOfAthwartLine());
    return height;
  }

  Line getMedian(Point first, Point second, Point third) const {
    Point cent_side((first.x + third.x) / 2.0, (first.y + third.y) / 2.0);
    Line ans = getLine(second, cent_side);
    return ans;
  }

  Line getBisector(Point first, Point second, Point third) const {
    double a_side = first.getLength(second);
    double b_side = second.getLength(third);
    double c_side = third.getLength(first);
    double ratio = a_side / (a_side + b_side);
    Line side = getLine(first, third);
    std::pair<Point, Point> needed = side.getPointsAtDistance(ratio * c_side, first);
    Point point = third.getTheNearest(needed.first, needed.second);
    Line ans = getLine(second, point);
    return ans;
  }

  Circle circumscribedCircle() const {
    Line a_side = getLine(vertices_[0], vertices_[1]);
    Line b_side = getLine(vertices_[1], vertices_[2]);
    Point cent_a((vertices_[0].x + vertices_[1].x) / 2.0, (vertices_[0].y + vertices_[1].y) / 2.0);
    Point cent_b((vertices_[1].x + vertices_[2].x) / 2.0, (vertices_[1].y + vertices_[2].y) / 2.0);
    Line athwart_a(cent_a, a_side.getAngleCoefficientOfAthwartLine());
    Line athwart_b(cent_b, b_side.getAngleCoefficientOfAthwartLine());
    Point cent = athwart_a.getIntersectionPoint(athwart_b);
    double rad = cent.getLength(vertices_[0]);
    Circle circ(cent, rad);
    return circ;
  }

  Circle inscribedCircle() const {
    Line first_bis = getBisector(vertices_[0], vertices_[1], vertices_[2]);
    Line second_bis = getBisector(vertices_[1], vertices_[2], vertices_[0]);
    Point cent = first_bis.getIntersectionPoint(second_bis);
    Line a_side = getLine(vertices_[0], vertices_[1]);
    Line athwart_a(cent, a_side.getAngleCoefficientOfAthwartLine());
    Point touch_point = athwart_a.getIntersectionPoint(a_side);
    double rad = cent.getLength(touch_point);
    Circle circ(cent, rad);
    return circ;
  }

  Point centroid() const {
    Line first_med = getMedian(vertices_[0], vertices_[1], vertices_[2]);
    Line second_med = getMedian(vertices_[1], vertices_[2], vertices_[0]);
    Point result = first_med.getIntersectionPoint(second_med);
    return result;
  }

  Point orthocenter() const {
    Line first_height = getHeight(vertices_[0], vertices_[1], vertices_[2]);
    Line second_height = getHeight(vertices_[1], vertices_[2], vertices_[0]);
    Point result = first_height.getIntersectionPoint(second_height);
    return result;
  }

  Line EulerLine() const {
    Point center_circum = circumscribedCircle().center();
    Line result = getLine(center_circum, orthocenter());
    return result;
  }

  Circle ninePointsCircle() const {
    Point cent_circum = circumscribedCircle().center();
    Point orthocent = orthocenter();
    Point cent((cent_circum.x + orthocent.x) / 2.0, (cent_circum.y + orthocent.y) / 2.0);
    double rad = circumscribedCircle().radius() / 2.0;
    Circle circ(cent, rad);
    return circ;
  }
  ~Triangle() = default;
};
